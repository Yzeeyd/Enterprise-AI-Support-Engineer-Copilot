import pytest

from app.backend.search.client import (
    get_opensearch_client
)

from app.backend.search.index import (
    INDEX_NAME
)

from app.backend.search.pipeline import (
    PIPELINE_NAME
)

from app.backend.embeddings import (
    get_embeddings_model
)

from app.backend.rag.hybrid_retriever import (
    HybridRetriever
)


@pytest.mark.integration
def test_opensearch_is_available():

    client = get_opensearch_client()

    assert client.ping() is True


@pytest.mark.integration
def test_knowledge_base_exists_and_has_documents():

    client = get_opensearch_client()

    assert client.indices.exists(
        index=INDEX_NAME
    )

    result = client.count(
        index=INDEX_NAME
    )

    assert result["count"] > 0


@pytest.mark.integration
def test_hybrid_pipeline_exists():

    client = get_opensearch_client()

    response = (
        client.transport.perform_request(
            method="GET",
            url=(
                f"/_search/pipeline/"
                f"{PIPELINE_NAME}"
            )
        )
    )

    assert PIPELINE_NAME in response


@pytest.mark.integration
def test_hybrid_retrieval_returns_results():

    client = get_opensearch_client()

    embeddings = get_embeddings_model()

    retriever = HybridRetriever(
        client=client,
        embedding_model=embeddings
    )

    results = retriever.retrieve(
        query="كيف أغير كلمة المرور؟",
        k=5
    )

    assert len(results) > 0

    for hit in results:

        assert "_source" in hit

        source = hit["_source"]

        assert "document_id" in source
        assert "chunk_id" in source
        assert "content" in source

        assert source["content"].strip()


@pytest.mark.integration
def test_password_query_retrieves_relevant_document():

    client = get_opensearch_client()

    embeddings = get_embeddings_model()

    retriever = HybridRetriever(
        client=client,
        embedding_model=embeddings
    )

    results = retriever.retrieve(
        query="كيف أغير كلمة المرور؟",
        k=5
    )

    document_ids = {
        hit["_source"]["document_id"]
        for hit in results
    }

    expected_documents = {
        "01_سياسة_كلمات_المرور_والمصادقة.pdf",
        "02_دليل_استعادة_الحساب_ومشاكل_تسجيل_الدخول.pdf"
    }

    assert (
        document_ids
        & expected_documents
    )