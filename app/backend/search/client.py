from opensearchpy import OpenSearch
import os
from dotenv import load_dotenv
load_dotenv()

def get_opensearch_client() -> OpenSearch:
    return OpenSearch(
        hosts=[
            {
                "host": os.getenv("OPENSEARCH_HOST"),
                "port": int(os.getenv("OPENSEARCH_PORT"))
            }
        ],
        use_ssl=False,
        verify_certs=False
    )