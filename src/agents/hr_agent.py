"""Agente RAG de Recursos Humanos."""

from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable

from src.agents.rag_agent import build_rag_agent
from src.config import DOMAINS

EXTRA_INSTRUCTIONS = """6. Las consultas sobre salud, licencias o situaciones personales son \
sensibles: respondé con empatía y, si corresponde, mencioná al People Partner o al \
canal confidencial EthicsLine.
7. El reembolso de gastos lo procesa Finance, aunque la aprobación de una \
capacitación sea de RR. HH.: aclaralo cuando aplique."""


def create_hr_agent(retriever: BaseRetriever, llm: BaseChatModel) -> Runnable:
    return build_rag_agent("hr", DOMAINS["hr"].name, retriever, llm, EXTRA_INSTRUCTIONS)
