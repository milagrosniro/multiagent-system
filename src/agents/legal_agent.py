"""Agente RAG de Legal y Compliance."""

from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable

from src.agents.rag_agent import build_rag_agent
from src.config import DOMAINS

EXTRA_INSTRUCTIONS = """6. Brindás información sobre las políticas internas, no asesoramiento \
legal personalizado: para casos concretos, derivá a LegalDesk o legal@nubesoft.com.
7. Ante reclamos formales, requerimientos de autoridades o posibles brechas de datos, \
remarcá los plazos y que no se debe responder sin intervención de Legal."""


def create_legal_agent(retriever: BaseRetriever, llm: BaseChatModel) -> Runnable:
    return build_rag_agent("legal", DOMAINS["legal"].name, retriever, llm, EXTRA_INSTRUCTIONS)
