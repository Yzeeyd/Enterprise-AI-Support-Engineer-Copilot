from opensearchpy.helpers import bulk

from app.backend.config import settings
from app.backend.search.index import INDEX_NAME


class OpenSearchRepository:

    def __init__(
        self,
        client,
        embedding_model
    ):
        self.client = client
        self.embedding_model = embedding_model


    def document_exists(
        self,
        document_id: str
    ) -> bool:

        response = self.client.count(
            index=INDEX_NAME,
            body={
                "query": {
                    "term": {
                        "document_id":
                            document_id
                    }
                }
            }
        )

        return response["count"] > 0


    def delete_document(
        self,
        document_id: str
    ) -> None:

        response = self.client.search(
            index=INDEX_NAME,
            body={
                "_source": False,
                "size": 1000,
                "query": {
                    "term": {
                        "document_id":
                            document_id
                    }
                }
            }
        )

        hits = response[
            "hits"
        ][
            "hits"
        ]

        if not hits:
            return

        actions = [
            {
                "_op_type": "delete",
                "_index": INDEX_NAME,
                "_id": hit["_id"]
            }
            for hit in hits
        ]

        bulk(
            self.client,
            actions
        )


    def index_chunks(
        self,
        chunks,
        document_id: str
    ) -> list[str]:

        if not chunks:
            return []

        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        vectors = (
            self.embedding_model
            .embed_documents(texts)
        )

        actions = []
        chunk_ids = []

        for index, (
            chunk,
            vector
        ) in enumerate(
            zip(chunks, vectors)
        ):

            chunk_id = (
                f"{document_id}::chunk_{index}"
            )

            document = {
                "chunk_id":
                    chunk_id,

                "document_id":
                    document_id,

                "content":
                    chunk.page_content,

                "embedding":
                    vector,

                "metadata":
                    chunk.metadata
            }

            actions.append(
                {
                    "_op_type": "index",
                    "_index": INDEX_NAME,
                    "_id": chunk_id,
                    "_source": document
                }
            )

            chunk_ids.append(
                chunk_id
            )

        bulk(
            self.client,
            actions
        )

        return chunk_ids


    def refresh(
        self
    ) -> None:

        # OpenSearch Serverless does not expose
        # the regular _refresh API.
        if (
            settings.opensearch_provider
            == "serverless"
        ):
            return

        self.client.indices.refresh(
            index=INDEX_NAME
        )