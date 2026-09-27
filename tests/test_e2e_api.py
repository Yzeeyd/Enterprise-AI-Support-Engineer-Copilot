import os

import httpx
import pytest


BASE_URL = os.getenv(
    "E2E_BASE_URL",
    "http://localhost:8000"
)


@pytest.mark.e2e
def test_health_endpoint():

    response = httpx.get(
        f"{BASE_URL}/health",
        timeout=10
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }


@pytest.mark.e2e
def test_chat_end_to_end():

    response = httpx.post(
        f"{BASE_URL}/api/v1/chat",
        json={
            "question": "كيف أغير كلمة المرور؟",
            "k": 5
        },
        timeout=120
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data

    assert isinstance(
        data["answer"],
        str
    )

    assert data["answer"].strip()

    assert isinstance(
        data["sources"],
        list
    )

    assert len(
        data["sources"]
    ) > 0


    filenames = {
        source["filename"]
        for source in data["sources"]
    }

    expected_documents = {
        "01_سياسة_كلمات_المرور_والمصادقة.pdf",
        "02_دليل_استعادة_الحساب_ومشاكل_تسجيل_الدخول.pdf"
    }

    assert (
        filenames
        & expected_documents
    )