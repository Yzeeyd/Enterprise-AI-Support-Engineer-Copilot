from .index import INDEX_NAME


class OpenSearchRepository:

    def __init__(
        self,
        client,
        embedding_model
    ):
        self.client = client
        self.embedding_model = embedding_model

    def delete_chunks(
    self,
    chunk_ids: list[str]
    ):

        for chunk_id in chunk_ids:

            self.client.delete(
                index=INDEX_NAME,
                id=chunk_id,
                ignore=[404]
            )
    
    def index_chunks(
        self,
        chunks,
        document_id: str
    ) -> list[str]:

        chunk_ids = []

        for index, chunk in enumerate(chunks):

            chunk_id = (
                f"{document_id}::chunk_{index}"
            )

            vector = (
                self.embedding_model
                .embed_query(
                    chunk.page_content
                )
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

            self.client.index(
                index=INDEX_NAME,
                id=chunk_id,
                body=document
            )

            chunk_ids.append(
                chunk_id
            )

        return chunk_ids