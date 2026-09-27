import boto3

from opensearchpy import (
    AWSV4SignerAuth,
    OpenSearch,
    RequestsHttpConnection
)

from app.backend.config import settings


def get_local_opensearch_client() -> OpenSearch:

    return OpenSearch(
        hosts=[
            {
                "host":
                    settings.opensearch_host,

                "port":
                    settings.opensearch_port
            }
        ],

        use_ssl=False,
        verify_certs=False,

        timeout=10,
        max_retries=3,
        retry_on_timeout=True
    )


def get_serverless_opensearch_client() -> OpenSearch:

    session = boto3.Session(
        region_name=settings.aws_region
    )

    credentials = (
        session.get_credentials()
    )

    if credentials is None:
        raise RuntimeError(
            "AWS credentials were not found."
        )

    auth = AWSV4SignerAuth(
        credentials,
        settings.aws_region,
        "aoss"
    )

    return OpenSearch(
        hosts=[
            {
                "host":
                    settings.opensearch_host,
                "port": 443
            }
        ],

        http_auth=auth,

        use_ssl=True,
        verify_certs=True,

        connection_class=(
            RequestsHttpConnection
        ),

        pool_maxsize=20,

        timeout=30,

        max_retries=3,
        retry_on_timeout=True
    )


def get_opensearch_client() -> OpenSearch:

    if (
        settings.opensearch_provider
        == "local"
    ):

        return (
            get_local_opensearch_client()
        )


    if (
        settings.opensearch_provider
        == "serverless"
    ):

        return (
            get_serverless_opensearch_client()
        )


    raise ValueError(
        "Unsupported OpenSearch provider: "
        f"{settings.opensearch_provider}"
    )