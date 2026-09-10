from langchain_chroma import Chroma
from pathlib import Path
import os


def VectorStore(embeddings_model:str):
    """Create a vector store from the document chunks and embeddings model.
    
    args:
        embeddings_model: The embeddings model to use for creating the vector store."""

    directoryBase = Path(os.getenv("ABSALUTEPATH")) / "data" / "database"

    # Create a vector store from the document chunks and embeddings model
    vector_store = Chroma(
        collection_name="KnowledgeBase",
        embedding_function=embeddings_model,
        persist_directory=directoryBase,
    )
    return vector_store