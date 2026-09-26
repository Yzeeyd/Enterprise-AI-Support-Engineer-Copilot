import os

from langchain_ollama import ChatOllama

from app.backend.llm.base import BaseLLM


class OllamaLLM(BaseLLM):

    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0.1
    ):
        self.model_name = (
            model
            or os.getenv("OLLAMA_LLM_MODEL")
            or "qwen3:8b"
        )

        self.client = ChatOllama(
            model=self.model_name,
            temperature=temperature,
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434"
            )
        )

    def generate(
        self,
        prompt: str
    ) -> str:
        response = self.client.invoke(prompt)
        return response.content


if __name__ == "__main__":

    llm = OllamaLLM()

    response = llm.generate(
        "اشرح RAG بجملة واحدة."
    )

    print(response)