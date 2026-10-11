"""BONUS: agente evaluador (LLM-as-a-judge) integrado con la Score API de Langfuse.

Para cada respuesta de un agente RAG, el evaluador puntúa de 1 a 10:
- relevance:     ¿responde lo que se preguntó?
- completeness:  ¿cubre todas las partes de la consulta?
- accuracy:      ¿cada afirmación está respaldada por el contexto recuperado?
- quality_score: puntaje global de 1 a 10 (el que pide la consigna).

Los puntajes se registran como scores en la misma traza de Langfuse de la
consulta, junto con un flag `needs_human_review` para las respuestas bajo el umbral.
"""

from typing import Optional

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from pydantic import BaseModel, Field

from src.config import QUALITY_REVIEW_THRESHOLD


class QualityEvaluation(BaseModel):
    relevance: int = Field(ge=1, le=10, description="Relevancia respecto de la consulta.")
    completeness: int = Field(ge=1, le=10, description="Completitud de la respuesta.")
    accuracy: int = Field(ge=1, le=10, description="Fidelidad al contexto recuperado.")
    overall_score: int = Field(ge=1, le=10, description="Calidad global de 1 a 10.")
    reasoning: str = Field(description="Justificación breve de los puntajes.")


JUDGE_SYSTEM_PROMPT = """Sos un evaluador de calidad de un sistema de soporte interno. \
Recibís una CONSULTA, el CONTEXTO que recuperó el sistema de la documentación \
interna y la RESPUESTA final que se le daría a la persona. Puntuá con enteros de 1 a 10.

Rúbrica:
- relevance: 9-10 responde directamente lo preguntado; 6-8 responde con algo de \
información de más o de menos; 3-5 responde parcialmente otra cosa; 1-2 no responde.
- completeness: 9-10 cubre todas las partes de la consulta con los datos clave \
(plazos, montos, pasos, canales); 6-8 le falta un detalle menor; 3-5 omite partes \
importantes; 1-2 casi no aporta información útil.
- accuracy: 9-10 todas las afirmaciones están respaldadas por el CONTEXTO; 6-8 hay \
una imprecisión menor; 3-5 hay un dato inventado o contradictorio con el contexto; \
1-2 la respuesta contradice el contexto o es mayormente inventada.
- overall_score: calidad global para enviarla a la persona, ponderando más la accuracy \
(una respuesta inventada nunca debe superar 4).

Casos especiales: si el CONTEXTO no contiene la información y la RESPUESTA lo admite \
honestamente en vez de inventar, la accuracy es alta (8-10) aunque la completeness sea \
baja. Sé estricto y consistente."""

JUDGE_HUMAN_PROMPT = """CONSULTA:
{question}

CONTEXTO RECUPERADO:
{context}

RESPUESTA A EVALUAR:
{answer}"""


def build_judge(llm: BaseChatModel) -> Runnable:
    prompt = ChatPromptTemplate.from_messages(
        [("system", JUDGE_SYSTEM_PROMPT), ("human", JUDGE_HUMAN_PROMPT)]
    )
    return (prompt | llm.with_structured_output(QualityEvaluation)).with_config(
        run_name="quality_judge"
    )


class ResponseEvaluator:
    """Evalúa respuestas y, si hay cliente de Langfuse, registra los scores en la traza."""

    def __init__(
        self,
        llm: BaseChatModel,
        langfuse=None,
        review_threshold: int = QUALITY_REVIEW_THRESHOLD,
    ):
        self.judge = build_judge(llm)
        self.langfuse = langfuse
        self.review_threshold = review_threshold

    def evaluate(self, question: str, answer: str, context: str, config=None) -> QualityEvaluation:
        return self.judge.invoke(
            {"question": question, "answer": answer, "context": context or "(sin contexto)"},
            config=config,
        )

    def evaluate_and_score(
        self,
        question: str,
        answer: str,
        context: str,
        trace_id: Optional[str] = None,
    ) -> dict:
        """Evalúa y registra los scores en Langfuse.

        - Sin `trace_id`: el evaluador se anida en la traza activa (uso dentro de `ask`).
        - Con `trace_id`: se adjunta a una traza ya existente (evaluación a posteriori).
        """
        if self.langfuse is None:
            evaluation = self.evaluate(question, answer, context)
            return self._summary(evaluation, trace_id=None)

        from langfuse.langchain import CallbackHandler

        trace_context = {"trace_id": trace_id} if trace_id else None
        with self.langfuse.start_as_current_observation(
            trace_context=trace_context,
            name="quality_evaluator",
            as_type="evaluator",
            input={"question": question, "answer": answer},
        ) as observation:
            evaluation = self.evaluate(
                question, answer, context, config={"callbacks": [CallbackHandler()]}
            )
            summary = self._summary(evaluation, trace_id=observation.trace_id)
            observation.update(output=summary)

        self._push_scores(summary)
        return summary

    def _summary(self, evaluation: QualityEvaluation, trace_id: Optional[str]) -> dict:
        return {
            "trace_id": trace_id,
            "relevance": evaluation.relevance,
            "completeness": evaluation.completeness,
            "accuracy": evaluation.accuracy,
            "quality_score": evaluation.overall_score,
            "needs_human_review": evaluation.overall_score < self.review_threshold,
            "reasoning": evaluation.reasoning,
        }

    def _push_scores(self, summary: dict) -> None:
        trace_id = summary["trace_id"]
        comment = summary["reasoning"]
        for name in ("relevance", "completeness", "accuracy", "quality_score"):
            self.langfuse.create_score(
                trace_id=trace_id,
                name=name,
                value=float(summary[name]),
                data_type="NUMERIC",
                comment=comment,
            )
        self.langfuse.create_score(
            trace_id=trace_id,
            name="needs_human_review",
            value=1.0 if summary["needs_human_review"] else 0.0,
            data_type="BOOLEAN",
            comment=f"Umbral: quality_score < {self.review_threshold}",
        )
