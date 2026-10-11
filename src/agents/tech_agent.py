"""Agente RAG de IT Support / Tecnología."""

from langchain_core.language_models import BaseChatModel
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import Runnable

from src.agents.rag_agent import build_rag_agent
from src.config import DOMAINS

EXTRA_INSTRUCTIONS = """6. Para problemas técnicos, dá primero los pasos de autodiagnóstico \
y después el canal de escalamiento (portal de IT, #it-help o mesa de ayuda) con la \
prioridad que corresponda.
7. Ante posibles incidentes de seguridad (phishing, pérdida de equipos, credenciales \
filtradas), indicá SIEMPRE reportarlo de inmediato en #security-incidents.
8. Nunca pidas ni sugieras compartir contraseñas."""


def create_tech_agent(retriever: BaseRetriever, llm: BaseChatModel) -> Runnable:
    return build_rag_agent("tech", DOMAINS["tech"].name, retriever, llm, EXTRA_INSTRUCTIONS)
