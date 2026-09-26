from app.backend.config import settings

from app.backend.search.client import (
    get_opensearch_client
)

from app.backend.search.index import (
    create_index
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


def index_documents_pipeline():

    client = get_opensearch_client()

    embeddings = get_embeddings_model()

    probe_vector = (
        embeddings.embed_query(
            "dimension probe"
        )
    )

    create_index(
        client=client,
        embedding_dimension=len(
            probe_vector
        )
    )

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

    return service.ingest_folder()


if __name__ == "__main__":
    print(
        index_documents_pipeline()
    )