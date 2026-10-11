"""Agente RAG de Finanzas."""

from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable

from src.agents.rag_agent import build_rag_agent
from src.config import DOMAINS

EXTRA_INSTRUCTIONS = """6. Cuando menciones montos, incluí siempre la moneda y la unidad \
(por persona, por noche, por mes) exactamente como figuran en la documentación.
7. Indicá los plazos y el nivel de aprobación que aplica al monto consultado.
8. El sueldo y el recibo de sueldo son de Payroll (RR. HH.), no de Finance: \
aclaralo si te preguntan por eso."""


def create_finance_agent(retriever: BaseRetriever, llm: BaseChatModel) -> Runnable:
    return build_rag_agent(
        "finance", DOMAINS["finance"].name, retriever, llm, EXTRA_INSTRUCTIONS
    )
