from app.backend.config import settings


def get_embeddings_model():

    if (
        settings.embedding_provider
        == "ollama"
    ):

        from app.backend.embeddings.ollama import (
            get_embeddings_model
            as get_ollama_embeddings
        )

        return get_ollama_embeddings()


    if (
        settings.embedding_provider
        == "bedrock"
    ):

        from app.backend.embeddings.bedrock import (
            BedrockEmbeddings
        )

        return BedrockEmbeddings()


    raise ValueError(
        "Unsupported embedding provider: "
        f"{settings.embedding_provider}"
    )


__all__ = [
    "get_embeddings_model"
]