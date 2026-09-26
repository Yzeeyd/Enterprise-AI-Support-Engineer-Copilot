from functools import lru_cache

from app.backend.search.client import get_opensearch_client
from app.backend.embeddings import get_embeddings_model
from app.backend.rag.hybrid_retriever import HybridRetriever
from app.backend.rag.service import RAGService


@lru_cache
def get_rag_service() -> RAGService:

    client = get_opensearch_client()
    embeddings = get_embeddings_model()

    retriever = HybridRetriever(
        client=client,
        embedding_model=embeddings
    )

    return RAGService(
        retriever=retriever
    )