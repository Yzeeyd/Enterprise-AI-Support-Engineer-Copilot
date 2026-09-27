from app.backend.config import settings


def get_llm():

    if settings.llm_provider == "ollama":

        from app.backend.llm.ollama import (
            OllamaLLM
        )

        return OllamaLLM()


    if settings.llm_provider == "bedrock":

        from app.backend.llm.bedrock import (
            BedrockLLM
        )

        return BedrockLLM()


    raise ValueError(
        "Unsupported LLM provider: "
        f"{settings.llm_provider}"
    )