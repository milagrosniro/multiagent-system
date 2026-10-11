"""Carga de documentos por dominio, chunking y vector stores FAISS persistidos."""

import hashlib
import json
from pathlib import Path

from langchain_community.document_loaders import CSVLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    CHUNK_OVERLAP_TOKENS,
    CHUNK_SIZE_TOKENS,
    DATA_DIR,
    DOMAINS,
    VECTORSTORE_DIR,
)

TEXT_EXTENSIONS = {".md", ".txt"}


def _load_file(path: Path) -> list[Document]:
    suffix = path.suffix.lower()
    if suffix in TEXT_EXTENSIONS:
        return TextLoader(str(path), encoding="utf-8").load()
    if suffix == ".csv":
        # Cada fila del CSV es un Document independiente (una FAQ o un límite).
        return CSVLoader(str(path), encoding="utf-8").load()
    if suffix == ".pdf":
        from langchain_community.document_loaders import PyPDFLoader  # requiere pypdf

        return PyPDFLoader(str(path)).load()
    return []


def domain_files(domain_key: str) -> list[Path]:
    folder = DATA_DIR / DOMAINS[domain_key].folder
    return sorted(p for p in folder.iterdir() if p.is_file() and not p.name.startswith("."))


def load_domain_documents(domain_key: str) -> list[Document]:
    docs: list[Document] = []
    for path in domain_files(domain_key):
        for doc in _load_file(path):
            doc.metadata.update({"domain": domain_key, "source": path.name})
            docs.append(doc)
    return docs


def build_splitter() -> RecursiveCharacterTextSplitter:
    # Medimos en tokens (tiktoken) y no en caracteres: es la unidad real que
    # consume el modelo y la que limita la ventana de contexto.
    return RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=CHUNK_SIZE_TOKENS,
        chunk_overlap=CHUNK_OVERLAP_TOKENS,
        separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "],
    )


def split_domain(domain_key: str) -> list[Document]:
    chunks = build_splitter().split_documents(load_domain_documents(domain_key))
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"{domain_key}-{i:03d}"
    return chunks


def _fingerprint(domain_key: str, embeddings: Embeddings) -> str:
    """Hash de los archivos + configuración: si cambia algo, se reconstruye el índice."""
    h = hashlib.sha256()
    for path in domain_files(domain_key):
        h.update(path.name.encode())
        h.update(path.read_bytes())
    model = getattr(embeddings, "model", type(embeddings).__name__)
    h.update(f"{CHUNK_SIZE_TOKENS}|{CHUNK_OVERLAP_TOKENS}|{model}".encode())
    return h.hexdigest()


def build_or_load_vectorstore(
    domain_key: str, embeddings: Embeddings, persist: bool = True
) -> tuple[FAISS, int]:
    """Devuelve (vector store, cantidad de chunks). Reutiliza el índice en disco si está al día."""
    index_dir = VECTORSTORE_DIR / domain_key
    meta_path = index_dir / "meta.json"
    fingerprint = _fingerprint(domain_key, embeddings)

    if persist and meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("fingerprint") == fingerprint:
            # El índice lo generamos nosotros mismos, por eso es seguro deserializarlo.
            store = FAISS.load_local(
                str(index_dir), embeddings, allow_dangerous_deserialization=True
            )
            return store, meta["n_chunks"]

    chunks = split_domain(domain_key)
    store = FAISS.from_documents(chunks, embeddings)
    if persist:
        index_dir.mkdir(parents=True, exist_ok=True)
        store.save_local(str(index_dir))
        meta_path.write_text(
            json.dumps({"fingerprint": fingerprint, "n_chunks": len(chunks)}),
            encoding="utf-8",
        )
    return store, len(chunks)
