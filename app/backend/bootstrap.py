import time

import requests

from app.backend.config import settings

from app.backend.search.client import (
    get_opensearch_client
)

from app.backend.search.index import (
    create_index
)

from app.backend.search.pipeline import (
    create_hybrid_pipeline
)

from app.backend.search.repository import (
    OpenSearchRepository
)

from app.backend.embeddings import (
    get_embeddings_model
)

from app.backend.ingestion.service import (
    IngestionService
)


def wait_for_opensearch(
    client,
    attempts: int = 60,
    delay: int = 2
) -> None:

    for _ in range(attempts):

        try:
            if client.ping():
                return

        except Exception:
            pass

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

    for _ in range(attempts):

        try:

            response = requests.get(
                url,
                timeout=3
            )

            if response.ok:
                return

        except requests.RequestException:
            pass

        time.sleep(delay)

    raise RuntimeError(
        "Ollama did not become ready."
    )


def bootstrap() -> None:

    print("Waiting for OpenSearch...")

    client = get_opensearch_client()

    wait_for_opensearch(client)

    print("OpenSearch ready.")

    print("Waiting for Ollama...")

    wait_for_ollama()

    print("Ollama ready.")

    embeddings = get_embeddings_model()

    probe_vector = embeddings.embed_query(
        "dimension probe"
    )

    created = create_index(
        client=client,
        embedding_dimension=len(
            probe_vector
        )
    )

    if created:
        print("OpenSearch index created.")
    else:
        print("OpenSearch index exists.")

    create_hybrid_pipeline(
        client
    )

    print("Hybrid RRF pipeline ready.")

    repository = OpenSearchRepository(
        client=client,
        embedding_model=embeddings
    )

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

    result = service.ingest_folder()

    print(
        "Ingestion complete:",
        result
    )


if __name__ == "__main__":
    bootstrap()