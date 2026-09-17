from app.backend.search.client import get_opensearch_client
from app.backend.search.index import INDEX_NAME


class BM25Retriever:

    def __init__(self, client):
        self.client = client


    def retrieve(
        self,
        query: str,
        k: int = 10
    ):

        body = {

            "size": k,

            "query": {

                "multi_match": {

                    "query": query,

                    "fields": [
                        "content",
                        "content.ar^2",
                        "content.en"
                    ]
                }
            }
        }

        response = self.client.search(
            index=INDEX_NAME,
            body=body
        )

        return response["hits"]["hits"]
    
if __name__ == "__main__":

    client = get_opensearch_client()

    retriever = BM25Retriever(client)

    results = retriever.retrieve(
        "كيف أغير كلمة المرور؟",
        k=1
    )
    for result in results:
        print(result["_source"]["content"])
        print("-----"*20)