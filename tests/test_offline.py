"""Smoke test offline: verifica el cableado del sistema sin API keys ni costo.

Usa embeddings determinísticos y un chat model falso que clasifica por keywords,
así se prueban el chunking, los vector stores, las ramas del RunnableBranch, el
formato de salida de los agentes y el evaluador.

Ejecutar:  python -m tests.test_offline    (o con pytest)
"""

import json

from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.runnables import RunnableLambda

from src.agents.orchestrator import RouteDecision
from src.config import DOMAINS, MIN_CHUNKS_PER_DOMAIN, TEST_QUERIES_PATH
from src.evaluator import QualityEvaluation
from src.ingest import split_domain
from src.multi_agent_system import MultiAgentSystem

KEYWORDS = {
    "hr": ["vacaciones", "licencia", "sueldo", "recibo", "renunci", "paternidad", "promoción"],
    "tech": ["vpn", "contraseña", "notebook", "phishing", "mfa", "yubikey"],
    "finance": ["reembolso", "viático", "hotel", "factura", "proveedor", "tarjeta"],
    "legal": ["nda", "contrato", "gpl", "datos personales", "regalo", "brecha"],
}


class KeywordFakeChatModel(BaseChatModel):
    """Chat model falso: texto fijo y salida estructurada por keywords."""

    @property
    def _llm_type(self) -> str:
        return "keyword-fake"

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        text = "Respuesta de prueba basada en el contexto recuperado. [fuente.md]"
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=text))])

    def with_structured_output(self, schema, **kwargs):
        def respond(prompt_value):
            query = prompt_value.to_messages()[-1].content.lower()
            if schema is RouteDecision:
                for dept, words in KEYWORDS.items():
                    if any(w in query for w in words):
                        return RouteDecision(department=dept, confidence=0.9, reasoning="kw")
                if "problema" in query:
                    return RouteDecision(department="tech", confidence=0.2, reasoning="vaga")
                return RouteDecision(department="out_of_scope", confidence=0.95, reasoning="-")
            if schema is QualityEvaluation:
                return QualityEvaluation(
                    relevance=8, completeness=7, accuracy=9, overall_score=8, reasoning="ok"
                )
            raise ValueError(schema)

        return RunnableLambda(respond)


def build_system() -> MultiAgentSystem:
    fake = KeywordFakeChatModel()
    return MultiAgentSystem(
        llm=fake,
        embeddings=DeterministicFakeEmbedding(size=128),
        evaluator_llm=fake,
        enable_langfuse=False,
        persist_vectorstores=False,
    )


def test_min_chunks_per_domain():
    for key in DOMAINS:
        assert len(split_domain(key)) >= MIN_CHUNKS_PER_DOMAIN, key


def test_test_queries_file():
    queries = json.loads(TEST_QUERIES_PATH.read_text(encoding="utf-8"))
    assert len(queries) >= 10
    expected = {q["expected_route"] for q in queries}
    assert {"hr", "tech", "finance", "legal", "out_of_scope"} <= expected


def test_routing_and_rag_output():
    system = build_system()
    cases = {
        "¿Cuántos días de vacaciones tengo?": ("hr", "hr_agent"),
        "No me conecta la VPN": ("tech", "tech_agent"),
        "¿Cuál es el tope de hotel en Madrid?": ("finance", "finance_agent"),
        "¿Puedo usar una librería GPL?": ("legal", "legal_agent"),
        "¿Quién ganó el partido?": ("out_of_scope", "out_of_scope"),
        "Tengo un problema": ("tech", "clarification"),
    }
    for question, (route, handler) in cases.items():
        result = system.ask(question)
        assert result["route"] == route, (question, result["route"])
        assert result["handled_by"] == handler, (question, result["handled_by"])
        if handler.endswith("_agent"):
            assert result["sources"] and result["context"]
            assert len(result["retrieved_chunks"]) == 4
            assert all(c.startswith(route) for c in result["retrieved_chunks"])
        else:
            assert result["sources"] == []


def test_evaluator():
    system = build_system()
    result = system.ask("¿Cuántos días de licencia por paternidad tengo?", evaluate=True)
    ev = result["evaluation"]
    assert ev["quality_score"] == 8 and ev["needs_human_review"] is False
    # Las respuestas sin RAG (fuera de alcance) no se evalúan.
    assert "evaluation" not in system.ask("¿Qué clima hace hoy?", evaluate=True)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"OK  {name}")
