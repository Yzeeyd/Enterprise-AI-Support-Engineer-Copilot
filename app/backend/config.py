import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:

    # -------------------------
    # Providers
    # -------------------------

    llm_provider: str = os.getenv(
        "LLM_PROVIDER",
        "ollama"
    ).lower()

    embedding_provider: str = os.getenv(
        "EMBEDDING_PROVIDER",
        "ollama"
    ).lower()


    # -------------------------
    # OpenSearch
    # -------------------------
    opensearch_provider: str = os.getenv(
        "OPENSEARCH_PROVIDER",
        "local"
    ).lower()
    
    opensearch_host: str = os.getenv(
        "OPENSEARCH_HOST",
        "localhost"
    )

    opensearch_port: int = int(
        os.getenv(
            "OPENSEARCH_PORT",
            "9200"
        )
    )

    index_name: str = os.getenv(
        "INDEX_NAME",
        "knowledge-base"
    )

    pipeline_name: str = os.getenv(
        "PIPELINE_NAME",
        "hybrid-rrf-pipeline"
    )


    # -------------------------
    # Data
    # -------------------------

    data_path: Path = Path(
        os.getenv(
            "DATAPATH",
            "data"
        )
    )

    index_state_path: Path = Path(
        os.getenv(
            "INDEX_STATE_PATH",
            "runtime/index_state.json"
        )
    )


    # -------------------------
    # Ollama
    # -------------------------

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


    # -------------------------
    # AWS
    # -------------------------

    aws_region: str = os.getenv(
        "AWS_REGION",
        "us-east-1"
    )

    bedrock_llm_model: str = os.getenv(
        "BEDROCK_LLM_MODEL",
        "qwen.qwen3-32b-v1:0"
    )

    bedrock_embedding_model: str = os.getenv(
        "BEDROCK_EMBEDDING_MODEL",
        "amazon.titan-embed-text-v2:0"
    )

    bedrock_embedding_dimensions: int = int(
        os.getenv(
            "BEDROCK_EMBEDDING_DIMENSIONS",
            "1024"
        )
    )


settings = Settings()