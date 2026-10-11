"""Ensambla el sistema completo: vector stores, agentes, orquestador, Langfuse y evaluador."""

from typing import Optional

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel

from src.agents.finance_agent import create_finance_agent
from src.agents.hr_agent import create_hr_agent
from src.agents.legal_agent import create_legal_agent
from src.agents.orchestrator import build_classifier, build_orchestrator
from src.agents.tech_agent import create_tech_agent
from src.config import (
    CHAT_MODEL,
    DOMAINS,
    EMBEDDING_MODEL,
    EVALUATOR_MODEL,
    RETRIEVER_FETCH_K,
    RETRIEVER_K,
    langfuse_configured,
)
from src.evaluator import ResponseEvaluator
from src.ingest import build_or_load_vectorstore

AGENT_FACTORIES = {
    "hr": create_hr_agent,
    "tech": create_tech_agent,
    "finance": create_finance_agent,
    "legal": create_legal_agent,
}

RAG_ROUTES = set(AGENT_FACTORIES)


class MultiAgentSystem:
    """Sistema multi-agente de soporte interno con routing, RAG, tracing y evaluación.

    Los modelos se pueden inyectar (por ejemplo, modelos falsos para tests offline);
    por defecto se usan los modelos de OpenAI definidos en `src/config.py`.
    """

    def __init__(
        self,
        llm: Optional[BaseChatModel] = None,
        embeddings: Optional[Embeddings] = None,
        evaluator_llm: Optional[BaseChatModel] = None,
        enable_langfuse: Optional[bool] = None,
        persist_vectorstores: bool = True,
    ):
        if llm is None or embeddings is None or evaluator_llm is None:
            from langchain_openai import ChatOpenAI, OpenAIEmbeddings

            llm = llm or ChatOpenAI(model=CHAT_MODEL, temperature=0)
            embeddings = embeddings or OpenAIEmbeddings(model=EMBEDDING_MODEL)
            evaluator_llm = evaluator_llm or ChatOpenAI(model=EVALUATOR_MODEL, temperature=0)
        self.llm = llm
        self.embeddings = embeddings

        # 1) Un vector store FAISS por dominio (conocimiento aislado).
        self.vectorstores, self.chunk_counts = {}, {}
        for key in DOMAINS:
            store, n_chunks = build_or_load_vectorstore(key, embeddings, persist_vectorstores)
            self.vectorstores[key] = store
            self.chunk_counts[key] = n_chunks

        # 2) Retrievers MMR: diversidad entre los k chunks devueltos.
        self.retrievers = {
            key: store.as_retriever(
                search_type="mmr",
                search_kwargs={"k": RETRIEVER_K, "fetch_k": RETRIEVER_FETCH_K},
            )
            for key, store in self.vectorstores.items()
        }

        # 3) Agentes RAG especializados.
        self.agents = {
            key: factory(self.retrievers[key], llm) for key, factory in AGENT_FACTORIES.items()
        }

        # 4) Orquestador = clasificador + enrutamiento condicional.
        self.classifier = build_classifier(llm)
        self.pipeline = build_orchestrator(self.classifier, self.agents)

        # 5) Observabilidad y evaluación.
        if enable_langfuse is None:
            enable_langfuse = langfuse_configured()
        self.langfuse = None
        if enable_langfuse:
            from langfuse import get_client

            self.langfuse = get_client()
        self.evaluator = ResponseEvaluator(evaluator_llm, self.langfuse)

    # ------------------------------------------------------------------ API --
    def ask(
        self,
        question: str,
        *,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        expected_route: Optional[str] = None,
        evaluate: bool = False,
        tags: Optional[list[str]] = None,
    ) -> dict:
        """Procesa una consulta de punta a punta y devuelve la respuesta con su metadata.

        Si Langfuse está configurado, toda la ejecución queda en una sola traza:
        clasificador -> rama elegida -> retriever -> generación -> (evaluador).
        """
        if self.langfuse is None:
            result = self.pipeline.invoke({"question": question})
            result["trace_id"] = None
            if evaluate and result["route"] in RAG_ROUTES:
                result["evaluation"] = self.evaluator.evaluate_and_score(
                    question, result["answer"], result["context"]
                )
            return result

        from langfuse import propagate_attributes
        from langfuse.langchain import CallbackHandler

        with self.langfuse.start_as_current_observation(
            name="support_request", as_type="agent", input={"question": question}
        ) as root:
            with propagate_attributes(
                trace_name="support_request",
                user_id=user_id,
                session_id=session_id,
                tags=["multi-agent-router", *(tags or [])],
            ):
                result = self.pipeline.invoke(
                    {"question": question}, config={"callbacks": [CallbackHandler()]}
                )
                result["trace_id"] = root.trace_id

                # Scores de routing: permiten filtrar y depurar misclassifications en la UI.
                root.score_trace(name="route", value=result["route"], data_type="CATEGORICAL")
                root.score_trace(
                    name="routing_confidence", value=result["confidence"], data_type="NUMERIC"
                )
                if expected_route is not None:
                    root.score_trace(
                        name="routing_correct",
                        value=1.0 if result["route"] == expected_route else 0.0,
                        data_type="BOOLEAN",
                        comment=f"esperado={expected_route} obtenido={result['route']}",
                    )

                if evaluate and result["route"] in RAG_ROUTES:
                    result["evaluation"] = self.evaluator.evaluate_and_score(
                        question, result["answer"], result["context"]
                    )

                output = {
                    "route": result["route"],
                    "handled_by": result["handled_by"],
                    "answer": result["answer"],
                    "sources": result["sources"],
                }
                root.update(
                    output=output,
                    metadata={
                        "confidence": result["confidence"],
                        "reasoning": result["reasoning"],
                        "retrieved_chunks": result["retrieved_chunks"],
                        "expected_route": expected_route,
                    },
                )
                root.set_trace_io(input={"question": question}, output=output)
        return result

    def flush(self) -> None:
        """Envía a Langfuse los eventos pendientes (imprescindible al final de un notebook)."""
        if self.langfuse is not None:
            self.langfuse.flush()
