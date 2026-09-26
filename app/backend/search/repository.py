from app.backend.search.index import (
    INDEX_NAME
)


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

        self.client.delete_by_query(
            index=INDEX_NAME,
            body={
                "query": {
                    "term": {
                        "document_id":
                            document_id
                    }
                }
            },
            conflicts="proceed",
            refresh=True
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
                "chunk_id": chunk_id,
                "document_id": document_id,
                "content":
                    chunk.page_content,
                "embedding": vector,
                "metadata":
                    chunk.metadata
            }

            self.client.index(
                index=INDEX_NAME,
                id=chunk_id,
                body=document
            )

            chunk_ids.append(
                chunk_id
            )

        return chunk_ids


    def refresh(self) -> None:

        self.client.indices.refresh(
            index=INDEX_NAME
        )