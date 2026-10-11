"""Fábrica genérica de agentes RAG especializados (LCEL).

Todos los agentes de dominio comparten la misma estructura —recuperar, armar
contexto, responder con citas— y solo cambian su base de conocimiento y sus
instrucciones. Por eso hay una sola fábrica y cada agente es una configuración.
"""

from operator import itemgetter

from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough

BASE_SYSTEM_PROMPT = """Sos el agente especializado de {department} de NubeSoft S.A., \
una empresa SaaS. Respondés consultas de personas empleadas y clientes usando \
EXCLUSIVAMENTE la documentación interna que aparece en el CONTEXTO.

Reglas:
1. Basá cada afirmación en el contexto. No inventes plazos, montos, nombres de \
herramientas ni procedimientos que no estén ahí.
2. Si el contexto no contiene la respuesta, decí claramente: "No encuentro esa \
información en la documentación de {department}" y sugerí a quién o por qué \
canal consultar, si el contexto lo indica.
3. Si la consulta tiene una parte que corresponde a otra área, respondé tu parte \
y aclarás qué área se encarga del resto.
4. Citá las fuentes al final con el formato [archivo].
5. Respondé en el mismo idioma de la consulta, de forma clara y concisa. Usá \
pasos numerados para los procedimientos.
{extra_instructions}"""

HUMAN_PROMPT = """CONTEXTO:
{context}

CONSULTA: {question}"""


def format_docs(docs: list[Document]) -> str:
    return "\n\n---\n\n".join(
        f"[{d.metadata.get('source', 'desconocido')}]\n{d.page_content}" for d in docs
    )


def _to_output(state: dict) -> dict:
    docs: list[Document] = state["docs"]
    return {
        "answer": state["answer"],
        "sources": sorted({d.metadata.get("source", "") for d in docs}),
        "context": state["context"],
        "retrieved_chunks": [d.metadata.get("chunk_id") for d in docs],
    }


def build_rag_agent(
    domain_key: str,
    department: str,
    retriever: BaseRetriever,
    llm: BaseChatModel,
    extra_instructions: str = "",
) -> Runnable:
    """Construye un agente RAG: {"question"} -> {"answer", "sources", "context", ...}."""
    prompt = ChatPromptTemplate.from_messages(
        [("system", BASE_SYSTEM_PROMPT), ("human", HUMAN_PROMPT)]
    ).partial(department=department, extra_instructions=extra_instructions)

    answer_chain = prompt | llm | StrOutputParser()

    chain = (
        RunnablePassthrough.assign(
            docs=(itemgetter("question") | retriever).with_config(
                run_name=f"{domain_key}_retriever"
            )
        )
        .assign(context=lambda x: format_docs(x["docs"]))
        .assign(answer=answer_chain.with_config(run_name=f"{domain_key}_generation"))
        | RunnableLambda(_to_output, name="format_output")
    )
    return chain.with_config(run_name=f"{domain_key}_rag_agent", tags=[f"agent:{domain_key}"])
