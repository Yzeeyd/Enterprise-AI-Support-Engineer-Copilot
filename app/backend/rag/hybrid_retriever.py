from app.backend.search.index import INDEX_NAME
from app.backend.search.pipeline import PIPELINE_NAME


class HybridRetriever:

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
        k: int = 5,
        candidates: int = 20
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

                "hybrid": {

                    "queries": [

                        # 1- BM25
                        {
                            "multi_match": {

                                "query": query,

                                "fields": [
                                    "content",
                                    "content.ar^2",
                                    "content.en"
                                ]
                            }
                        },

                        # 2- Vector
                        {
                            "knn": {

                                "embedding": {

                                    "vector": query_vector,
                                    "k": candidates
                                }
                            }
                        }
                    ]
                }
            }
        }

        response = self.client.search(

            index=INDEX_NAME,

            params={
                "search_pipeline": PIPELINE_NAME
            },

            body=body
        )

        return response["hits"]["hits"]



if __name__ == "__main__":

    from app.backend.search.client import (
        get_opensearch_client
    )

    from app.backend.embeddings import (
        get_embeddings_model
    )

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

    for rank, hit in enumerate(
        results,
        start=1
    ):

        source = hit["_source"]

        print(f"\nRank: {rank}")
        print(f"Score: {hit['_score']}")
        print(
            f"Document: "
            f"{source['document_id']}"
        )

        print(
            f"Content:\n"
            f"{source['content']}"
        )

        print("-" * 80)