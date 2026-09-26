from opensearchpy import OpenSearch

from app.backend.config import settings


def get_opensearch_client() -> OpenSearch:

    return OpenSearch(
        hosts=[
            {
                "host": settings.opensearch_host,
                "port": settings.opensearch_port
            }
        ],
        use_ssl=False,
        verify_certs=False,
        timeout=10,
        max_retries=3,
        retry_on_timeout=True
    )