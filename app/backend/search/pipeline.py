from app.backend.config import settings


PIPELINE_NAME = settings.pipeline_name


def create_hybrid_pipeline(
    client
) -> None:

    if (
        settings.opensearch_provider
        == "serverless"
    ):

        body = {
            "description": (
                "Hybrid BM25 + Vector search "
                "using score normalization"
            ),

            "phase_results_processors": [
                {
                    "normalization-processor": {

                        "normalization": {
                            "technique":
                                "min_max"
                        },

                        "combination": {
                            "technique":
                                "arithmetic_mean",

                            "parameters": {
                                "weights": [
                                    0.5,
                                    0.5
                                ]
                            }
                        }
                    }
                }
            ]
        }

    else:

        body = {
            "description": (
                "Hybrid BM25 + Vector "
                "search using RRF"
            ),

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
        url=(
            f"/_search/pipeline/"
            f"{PIPELINE_NAME}"
        ),
        body=body
    )