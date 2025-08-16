"""Cognition base package.

The cognition base provides domain knowledge to support the pipeline.
In the full ASI‑Arch system this is implemented as a retrieval‑
augmented generation (RAG) service backed by a vector database.  In
this skeleton the service simply returns static advice for any query.
"""

from .rag_service import RAGService  # noqa: F401
