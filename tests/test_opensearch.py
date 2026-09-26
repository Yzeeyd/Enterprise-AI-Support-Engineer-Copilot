from app.backend.search.client import get_opensearch_client
from app.backend.search.index import create_index
from app.backend.embeddings import get_embeddings_model


def test_opensearch_index():

    client = get_opensearch_client()

    embeddings = get_embeddings_model()

    probe_vector = embeddings.embed_query(
        "dimension probe"
    )

    create_index(
        client=client,
        embedding_dimension=len(probe_vector)
    )

    assert client.ping()