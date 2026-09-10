from langchain_chroma import Chroma
from pathlib import Path
import os

from langchain_ollama import OllamaEmbeddings


def VectorStore(embeddings_model) -> Chroma:
    """Create a vector store from the document chunks and embeddings model.
    
    args:
        embeddings_model: The embeddings model to use for creating the vector store."""

    
    directoryBase = Path(os.getenv("DATAPATH")) / "database"


    # Create a vector store from the document chunks and embeddings model
    vector_store = Chroma(
        collection_name="KnowledgeBase",
        embedding_function=embeddings_model,
        persist_directory=directoryBase,
    )
    return vector_store


def embeddings_model(model="qwen3-embedding:latest") -> object:
    """Create an embeddings model.
    
    args:
        None
    returns:
        An embeddings model object."""
    
    return OllamaEmbeddings(model="qwen3-embedding:latest")