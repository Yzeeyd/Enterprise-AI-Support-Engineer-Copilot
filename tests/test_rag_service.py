from app.backend.rag.service import RAGService


class FakeRetriever:
    def retrieve(self, query: str, k: int = 5):
        return [
            {
                "_score": 0.03,
                "_source": {
                    "document_id": "password_policy.pdf",
                    "chunk_id": "password_policy.pdf::chunk_0",
                    "content": "يمكن إعادة تعيين كلمة المرور عبر بوابة الاستعادة.",
                    "metadata": {
                        "filename": "password_policy.pdf",
                        "page": 0
                    }
                }
            }
        ]


class FakeLLM:
    def generate(self, prompt: str) -> str:
        assert "بوابة الاستعادة" in prompt

        return "يمكن إعادة تعيين كلمة المرور عبر بوابة الاستعادة [1]."


def test_rag_service_returns_answer_and_sources():

    service = RAGService(
        retriever=FakeRetriever(),
        llm=FakeLLM()
    )

    result = service.ask(
        "كيف أغير كلمة المرور؟"
    )

    assert "بوابة الاستعادة" in result["answer"]

    assert len(result["sources"]) == 1

    assert result["sources"][0]["id"] == 1

    assert (
        result["sources"][0]["filename"]
        == "password_policy.pdf"
    )