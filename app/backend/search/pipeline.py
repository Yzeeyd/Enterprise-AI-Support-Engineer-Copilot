import os

PIPELINE_NAME = os.environ.get("PIPELINE_NAME")


def create_hybrid_pipeline(client) -> None:

    body = {
        "description": "Hybrid BM25 + Vector search using RRF",

        "phase_results_processors": [
            {
                "score-ranker-processor": {
                    "combination": {
                        "technique": "rrf",
                        "rank_constant": 60
                    }
                }
            }
        ]
    }

    client.transport.perform_request(
        method="PUT",
        url=f"/_search/pipeline/{PIPELINE_NAME}",
        body=body
    )


if __name__ == "__main__":

    from app.backend.search.client import (
        get_opensearch_client
    )

    client = get_opensearch_client()

    create_hybrid_pipeline(client)

    print("Hybrid RRF pipeline created.")