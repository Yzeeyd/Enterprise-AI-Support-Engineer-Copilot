import os
from langchain_ollama import OllamaEmbeddings


def get_embeddings_model(
    model="qwen3-embedding:latest"
):
    return OllamaEmbeddings(
        model=model,
        base_url=os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434"
        )
    )