def get_llm():
    from app.backend.llm.ollama import OllamaLLM

    return OllamaLLM()