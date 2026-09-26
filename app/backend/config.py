import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    opensearch_host: str = os.getenv(
        "OPENSEARCH_HOST",
        "localhost"
    )

    opensearch_port: int = int(
        os.getenv("OPENSEARCH_PORT", "9200")
    )

    index_name: str = os.getenv(
        "INDEX_NAME",
        "knowledge-base"
    )

    pipeline_name: str = os.getenv(
        "PIPELINE_NAME",
        "hybrid-rrf-pipeline"
    )

    data_path: Path = Path(
        os.getenv("DATAPATH", "data")
    )

    index_state_path: Path = Path(
        os.getenv(
            "INDEX_STATE_PATH",
            "runtime/index_state.json"
        )
    )

    ollama_base_url: str = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434"
    )

    embedding_model: str = os.getenv(
        "OLLAMA_EMBEDDING_MODEL",
        "qwen3-embedding:latest"
    )

    llm_model: str = os.getenv(
        "OLLAMA_LLM_MODEL",
        "qwen3.5:9b"
    )


settings = Settings()