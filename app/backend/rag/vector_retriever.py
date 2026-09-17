from app.backend.search.index import INDEX_NAME
from app.backend.search.client import get_opensearch_client
# embeddings
from app.backend.embeddings import get_embeddings_model
class VectorRetriever:

    def __init__(
        self,
        client,
        embedding_model
    ):
        self.client = client
        self.embedding_model = embedding_model


    def retrieve(
        self,
        query: str,
        k: int = 10
    ):

        query_vector = (
            self.embedding_model
            .embed_query(query)
        )

        body = {
            "size": k,

            "_source": {
                "excludes": ["embedding"]
            },

            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_vector,
                        "k": k
                    }
                }
            }
        }

        response = self.client.search(
            index=INDEX_NAME,
            body=body
        )

        return response["hits"]["hits"]


if __name__ == "__main__":
    # Example usage
    query = "كلمة السر"
    top_k = 5
    
    retriever = VectorRetriever(client=get_opensearch_client(), embedding_model=get_embeddings_model())
    results = retriever.retrieve(query=query, k=top_k)

    print(f"Top {top_k} results for query '{query}':")
    for result in results:
        print(result)

