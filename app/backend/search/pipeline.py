from app.backend.config import settings


PIPELINE_NAME = settings.pipeline_name


def create_hybrid_pipeline(client) -> None:

    body = {
        "description":
            "Hybrid BM25 + Vector search using RRF",

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