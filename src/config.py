"""Configuración central del sistema: rutas, modelos, dominios y parámetros de RAG."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

DATA_DIR = PROJECT_ROOT / "data"
VECTORSTORE_DIR = PROJECT_ROOT / "vectorstores"
TEST_QUERIES_PATH = PROJECT_ROOT / "test_queries.json"

# --- Modelos -----------------------------------------------------------------
# gpt-4o-mini: barato, rápido y suficiente para clasificar y responder sobre
# contexto recuperado. Se puede cambiar sin tocar código vía .env.
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
EVALUATOR_MODEL = os.getenv("OPENAI_EVALUATOR_MODEL", CHAT_MODEL)
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# --- Parámetros de RAG -------------------------------------------------------
# Las políticas están escritas en secciones cortas y autocontenidas, por eso
# chunks chicos (~200 tokens) dan recuperaciones más precisas que chunks largos.
CHUNK_SIZE_TOKENS = 200
CHUNK_OVERLAP_TOKENS = 30
RETRIEVER_K = 4
RETRIEVER_FETCH_K = 20
MIN_CHUNKS_PER_DOMAIN = 50

# --- Routing -----------------------------------------------------------------
# Por debajo de este umbral el orquestador no adivina: pide una aclaración.
ROUTING_CONFIDENCE_THRESHOLD = 0.5

# --- Evaluación --------------------------------------------------------------
# Respuestas con puntaje global menor a este valor se marcan para revisión humana.
QUALITY_REVIEW_THRESHOLD = 6


@dataclass(frozen=True)
class Domain:
    key: str
    name: str
    folder: str
    description: str


DOMAINS: dict[str, Domain] = {
    "hr": Domain(
        key="hr",
        name="Recursos Humanos (HR)",
        folder="hr_docs",
        description=(
            "vacaciones, licencias, sueldo y recibo de sueldo (payroll), beneficios, "
            "seguro de salud, bono, revisión salarial, onboarding, renuncias, "
            "evaluación de desempeño, promociones, trabajo remoto, horarios, "
            "código de conducta y acoso laboral"
        ),
    ),
    "tech": Domain(
        key="tech",
        name="IT Support / Tecnología",
        folder="tech_docs",
        description=(
            "VPN, contraseñas, MFA, cuentas y accesos, notebooks y hardware, "
            "software, incidentes de producción, phishing, seguridad informática, "
            "mesa de ayuda y SLA de soporte"
        ),
    ),
    "finance": Domain(
        key="finance",
        name="Finanzas (Finance)",
        folder="finance_docs",
        description=(
            "reembolso de gastos, Spendly, viajes y viáticos, tarjetas corporativas, "
            "facturación y cobranza a clientes, compras y pagos a proveedores, "
            "presupuestos y cierre contable"
        ),
    ),
    "legal": Domain(
        key="legal",
        name="Legal y Compliance",
        folder="legal_docs",
        description=(
            "contratos, NDA, autoridad de firma, privacidad y protección de datos "
            "(GDPR), brechas de datos, propiedad intelectual, licencias open source, "
            "regalos, anticorrupción y conflictos de interés"
        ),
    ),
}


def openai_configured() -> bool:
    key = os.getenv("OPENAI_API_KEY", "")
    return bool(key) and not key.startswith("your-")


def langfuse_configured() -> bool:
    public = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    secret = os.getenv("LANGFUSE_SECRET_KEY", "")
    return (
        public.startswith("pk-lf-")
        and secret.startswith("sk-lf-")
        and "xxx" not in public
        and "xxx" not in secret
    )
