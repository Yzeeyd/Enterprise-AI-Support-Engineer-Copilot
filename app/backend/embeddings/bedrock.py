import json

import boto3

from app.backend.config import settings


class BedrockEmbeddings:

    def __init__(
        self,
        model: str | None = None,
        dimensions: int | None = None,
        normalize: bool = True
    ):

        self.model_name = (
            model
            or settings.bedrock_embedding_model
        )

        self.dimensions = (
            dimensions
            or settings.bedrock_embedding_dimensions
        )

        self.normalize = normalize


        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.aws_region
        )


    def _embed(
        self,
        text: str
    ) -> list[float]:

        body = {
            "inputText": text,
            "dimensions": self.dimensions,
            "normalize": self.normalize
        }


        response = self.client.invoke_model(
            modelId=self.model_name,

            contentType="application/json",
            accept="application/json",

            body=json.dumps(
                body
            )
        )


        response_body = json.loads(
            response["body"].read()
        )


        return response_body[
            "embedding"
        ]


    def embed_query(
        self,
        text: str
    ) -> list[float]:

        return self._embed(
            text
        )


    def embed_documents(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        return [
            self._embed(text)
            for text in texts
        ]