from app.backend.search.client import get_opensearch_client
from app.backend.search.index import create_index


client = get_opensearch_client()

create_index(client)

print("Index created successfully")