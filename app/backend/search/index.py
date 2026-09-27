from app.backend.config import settings


INDEX_NAME = settings.index_name


def create_index(
    client,
    embedding_dimension: int
) -> bool:

    if client.indices.exists(
        index=INDEX_NAME
    ):
        return False

    embedding_mapping = {
        "type": "knn_vector",
        "dimension": embedding_dimension
    }

    if settings.opensearch_provider == "serverless":

        embedding_mapping.update(
            {
                "space_type": "cosinesimil",
                "compression_level": "1x"
            }
        )

    else:

        embedding_mapping.update(
            {
                "method": {
                    "name": "hnsw",
                    "space_type": "cosinesimil",
                    "engine": "lucene",
                    "parameters": {
                        "ef_construction": 100,
                        "m": 16
                    }
                }
            }
        )

    body = {
        "settings": {
            "index": {
                "knn": True
            }
        },

        "mappings": {
            "properties": {

                "chunk_id": {
                    "type": "keyword"
                },

                "document_id": {
                    "type": "keyword"
                },

                "content": {
                    "type": "text",

                    "fields": {
                        "ar": {
                            "type": "text",
                            "analyzer": "arabic"
                        },

                        "en": {
                            "type": "text",
                            "analyzer": "english"
                        }
                    }
                },

                "embedding": embedding_mapping,

                "metadata": {
                    "type": "object"
                }
            }
        }
    }

    client.indices.create(
        index=INDEX_NAME,
        body=body
    )

    return True