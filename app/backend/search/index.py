from dotenv import load_dotenv
import os
load_dotenv()

INDEX_NAME = os.getenv("INDEX_NAME")

def create_index(
    client,
    embedding_dimension: int
):

    if client.indices.exists(
        index=INDEX_NAME
    ):
        return

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

                "embedding": {

                    "type": "knn_vector",

                    "dimension":
                        embedding_dimension,

                    "method": {

                        "name": "hnsw",

                        "space_type":
                            "cosinesimil",

                        "engine":
                            "lucene",

                        "parameters": {

                            "ef_construction": 100,

                            "m": 16
                        }
                    }
                },

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