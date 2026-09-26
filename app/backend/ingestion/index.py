import os
from pathlib import Path

from app.backend.search.client import (
    get_opensearch_client
)

from app.backend.search.index import (
    create_index
)

from app.backend.search.repository import (
    OpenSearchRepository
)

from app.backend.embeddings.ollama import (
    get_embeddings_model
)

from app.backend.ingestion.service import (
    IngestionService
)


def index_documents_pipeline():

    data_path = Path(
        os.getenv("DATAPATH")
    )

    documents_root = (
        data_path / "raw" / "doc"
    )

    state_path = (
        data_path / "index_state.json"
    )

    # Dependencies
    client = get_opensearch_client()
    embeddings = get_embeddings_model()

    # Make sure index exists
    probe_vector = embeddings.embed_query(
        "dimension probe"
    )

    create_index(
        client=client,
        embedding_dimension=len(probe_vector),
    )

    # Repository
    repository = OpenSearchRepository(
        client=client,
        embedding_model=embeddings,
    )

    # Ingestion Service
    service = IngestionService(
        repository=repository,
        documents_root=documents_root,
        state_path=state_path,
    )

    results = service.ingest_folder()

    print(results)


if __name__ == "__main__":
    index_documents_pipeline()