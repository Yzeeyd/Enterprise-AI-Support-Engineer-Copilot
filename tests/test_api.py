from fastapi.testclient import TestClient

from app.backend.main import app
from app.backend.api.dependencies import (
    get_rag_service
)


class FakeRAGService:

    def ask(
        self,
        question: str,
        k: int = 5
    ):
        return {
            "answer": "Test answer [1].",
            "sources": [
                {
                    "id": 1,
                    "document_id": "test.pdf",
                    "filename": "test.pdf",
                    "chunk_ids": [
                        "test.pdf::chunk_0"
                    ],
                    "score": 0.03
                }
            ]
        }


def override_rag_service():
    return FakeRAGService()


app.dependency_overrides[
    get_rag_service
] = override_rag_service


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }


def test_chat():

    response = client.post(
        "/api/v1/chat",
        json={
            "question": "كيف أغير كلمة المرور؟",
            "k": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == "Test answer [1]."

    assert len(data["sources"]) == 1