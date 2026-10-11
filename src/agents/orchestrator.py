"""Agente orquestador: clasifica la intención y enruta al agente RAG correcto.

Flujo (todo en LCEL):

    {"question"} -> classifier (structured output) -> RunnableBranch -> agente -> salida

- El clasificador devuelve un objeto Pydantic validado (departamento + confianza +
  razonamiento), así el routing nunca depende de parsear texto libre y el
  razonamiento queda visible en la traza de Langfuse para depurar errores.
- RunnableBranch es el enrutamiento condicional nativo de LangChain: cada rama es
  un nodo propio en la traza.
"""

from typing import Literal

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    Runnable,
    RunnableBranch,
    RunnableLambda,
    RunnablePassthrough,
)
from pydantic import BaseModel, Field

from src.config import DOMAINS, ROUTING_CONFIDENCE_THRESHOLD

Department = Literal["hr", "tech", "finance", "legal", "out_of_scope"]


class RouteDecision(BaseModel):
    """Decisión de routing del orquestador."""

    department: Department = Field(
        description="Departamento que debe responder la consulta."
    )
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confianza en la clasificación, entre 0 y 1."
    )
    reasoning: str = Field(
        description="Justificación breve (1 o 2 oraciones) de la clasificación."
    )


def _departments_block() -> str:
    return "\n".join(f"- {d.key}: {d.name}. Temas: {d.description}." for d in DOMAINS.values())


CLASSIFIER_SYSTEM_PROMPT = """Sos el orquestador de la mesa de soporte interna de NubeSoft \
S.A., una empresa SaaS. Tu única tarea es clasificar cada consulta en el departamento \
que debe responderla. No respondas la consulta.

Departamentos:
{departments}
- out_of_scope: consultas que no tienen relación con ningún departamento de la empresa \
(clima, deportes, recetas, conocimiento general, charla casual).

Criterios:
- Elegí el departamento que es DUEÑO del proceso o la política consultada, no el que \
aparece mencionado de pasada.
- Si la consulta toca dos áreas, elegí la de la acción principal que pide la persona.
- El sueldo, el recibo de sueldo y sus descuentos son de hr (Payroll), no de finance.
- Una pérdida o robo de equipo es primero un incidente de tech; las obligaciones de \
notificar una brecha de datos personales son de legal.
- Usá confianza menor a 0.5 solo si la consulta es tan vaga que no se puede saber \
qué área corresponde.
- La consulta puede estar en cualquier idioma o tener errores de tipeo.

Ejemplos:
- "¿Cuántos días de vacaciones me tocan?" -> hr (0.97)
- "No me anda la VPN desde el hotel" -> tech (0.97)
- "¿Cuál es el tope de hotel en Madrid?" -> finance (0.95)
- "Un cliente nos pidió firmar su propio NDA" -> legal (0.95)
- "Me aprobaron un curso, ¿cómo cargo el ticket para que me lo devuelvan?" -> finance (0.8)
- "Hay un error en los descuentos de mi recibo de sueldo" -> hr (0.9)
- "Me robaron la notebook en el tren" -> tech (0.85)
- "¿Puedo usar una librería con licencia GPL en el producto?" -> legal (0.9)
- "Tengo un problema" -> out_of_scope o el área más probable con confianza 0.2
- "¿Quién ganó el partido de ayer?" -> out_of_scope (0.98)"""


def build_classifier(llm: BaseChatModel) -> Runnable:
    """{"question"} -> RouteDecision"""
    prompt = ChatPromptTemplate.from_messages(
        [("system", CLASSIFIER_SYSTEM_PROMPT), ("human", "Consulta: {question}")]
    ).partial(departments=_departments_block())
    return (prompt | llm.with_structured_output(RouteDecision)).with_config(
        run_name="intent_classifier"
    )


OUT_OF_SCOPE_MESSAGE = (
    "Tu consulta no parece estar relacionada con ninguna de las áreas de soporte interno "
    "de NubeSoft. Puedo ayudarte con temas de: "
    + "; ".join(d.name for d in DOMAINS.values())
    + ". ¿Podrías reformularla?"
)

CLARIFICATION_MESSAGE = (
    "No pude identificar con seguridad a qué área corresponde tu consulta. "
    "¿Podrías darme más detalles? Por ejemplo, si se trata de "
    + ", ".join(d.name for d in DOMAINS.values())
    + "."
)


def _static_response(handled_by: str, message: str) -> Runnable:
    """Respuesta determinística (sin LLM) para los casos donde no se delega a un agente."""
    return RunnableLambda(
        lambda _: {
            "handled_by": handled_by,
            "answer": message,
            "sources": [],
            "context": "",
            "retrieved_chunks": [],
        },
        name=handled_by,
    )


def _finalize(state: dict) -> dict:
    route: RouteDecision = state["route"]
    return {
        "question": state["question"],
        "route": route.department,
        "confidence": route.confidence,
        "reasoning": route.reasoning,
        **state["result"],
    }


def build_orchestrator(
    classifier: Runnable,
    agents: dict[str, Runnable],
    confidence_threshold: float = ROUTING_CONFIDENCE_THRESHOLD,
) -> Runnable:
    """Pipeline completo: {"question"} -> dict con ruta, respuesta, fuentes y contexto."""

    def low_confidence(x: dict) -> bool:
        route: RouteDecision = x["route"]
        return route.department != "out_of_scope" and route.confidence < confidence_threshold

    branches: list = [(low_confidence, _static_response("clarification", CLARIFICATION_MESSAGE))]
    for key, agent in agents.items():
        tag_handler = RunnableLambda(lambda out, k=key: {"handled_by": f"{k}_agent", **out})
        branches.append((lambda x, k=key: x["route"].department == k, agent | tag_handler))

    router = RunnableBranch(
        *branches,
        _static_response("out_of_scope", OUT_OF_SCOPE_MESSAGE),  # rama por defecto
    ).with_config(run_name="conditional_router")

    return (
        RunnablePassthrough.assign(route=classifier)
        | RunnablePassthrough.assign(result=router)
        | RunnableLambda(_finalize, name="finalize")
    ).with_config(run_name="orchestrator")
