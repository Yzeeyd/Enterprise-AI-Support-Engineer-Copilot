import time

import requests

from app.backend.config import settings
from app.backend.search.client import get_opensearch_client
from app.backend.search.index import create_index
from app.backend.search.pipeline import create_hybrid_pipeline
from app.backend.search.repository import OpenSearchRepository
from app.backend.embeddings import get_embeddings_model
from app.backend.ingestion.service import IngestionService


def wait_for_opensearch(
    client,
    attempts: int = 20,
    delay: int = 2
) -> None:

    for attempt in range(1, attempts + 1):

        try:

            # OpenSearch Serverless does not
            if settings.opensearch_provider == "serverless":

                client.cat.indices(
                    format="json"
                )

                return

            # Local OpenSearch
            if client.ping():
                return

        except Exception as exc:

            print(
                f"OpenSearch attempt "
                f"{attempt}/{attempts} failed: "
                f"{exc}"
            )

        time.sleep(delay)

    raise RuntimeError(
        "OpenSearch did not become ready."
    )


def wait_for_ollama(
    attempts: int = 60,
    delay: int = 2
) -> None:

    url = (
        settings.ollama_base_url.rstrip("/")
        + "/api/tags"
    )

    for attempt in range(1, attempts + 1):

        try:

            response = requests.get(
                url,
                timeout=3
            )

            if response.ok:
                return

        except requests.RequestException as exc:

            print(
                f"Ollama attempt "
                f"{attempt}/{attempts} failed: "
                f"{exc}"
            )

        time.sleep(delay)

    raise RuntimeError(
        "Ollama did not become ready."
    )


def bootstrap() -> None:

    # ---------------------------------
    # OpenSearch
    # ---------------------------------

    print("Waiting for OpenSearch...")

    client = get_opensearch_client()

    wait_for_opensearch(
        client
    )

    print("OpenSearch ready.")


    # ---------------------------------
    # Ollama
    # ---------------------------------

    needs_ollama = (
        settings.llm_provider == "ollama"
        or
        settings.embedding_provider == "ollama"
    )

    if needs_ollama:

        print(
            "Waiting for Ollama..."
        )

        wait_for_ollama()

        print(
            "Ollama ready."
        )

    else:

        print(
            "Using AWS Bedrock. "
            "Skipping Ollama."
        )


    # ---------------------------------
    # Embeddings
    # ---------------------------------

    embeddings = (
        get_embeddings_model()
    )

    probe_vector = (
        embeddings.embed_query(
            "dimension probe"
        )
    )

    print(
        f"Embedding dimension: "
        f"{len(probe_vector)}"
    )


    # ---------------------------------
    # Index
    # ---------------------------------

    created = create_index(
        client=client,
        embedding_dimension=len(
            probe_vector
        )
    )

    if created:

        print(
            "OpenSearch index created."
        )

    else:

        print(
            "OpenSearch index exists."
        )


    # ---------------------------------
    # Hybrid Search Pipeline
    # ---------------------------------

    create_hybrid_pipeline(
        client
    )

    if (
        settings.opensearch_provider
        == "serverless"
    ):

        print(
            "Hybrid normalization "
            "pipeline ready."
        )

    else:

        print(
            "Hybrid RRF pipeline ready."
        )


    # ---------------------------------
    # Repository
    # ---------------------------------

    repository = (
        OpenSearchRepository(
            client=client,
            embedding_model=embeddings
        )
    )


    # ---------------------------------
    # Ingestion
    # ---------------------------------

    service = IngestionService(

        repository=repository,

        documents_root=(
            settings.data_path
            / "raw"
            / "doc"
        ),

        state_path=(
            settings.index_state_path
        )
    )


    print(
        "Starting document ingestion..."
    )

    result = (
        service.ingest_folder()
    )


    print(
        "Ingestion complete:"
    )

    print(
        result
    )


if __name__ == "__main__":

    bootstrap()