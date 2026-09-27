import boto3

from app.backend.config import settings
from app.backend.llm.base import BaseLLM


class BedrockLLM(BaseLLM):

    def __init__(
        self,
        model: str | None = None,
        temperature: float = 0.1,
        max_tokens: int = 1024
    ):

        self.model_name = (
            model
            or settings.bedrock_llm_model
        )

        self.temperature = temperature
        self.max_tokens = max_tokens

        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.aws_region
        )


    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.client.converse(
            modelId=self.model_name,

            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],

            inferenceConfig={
                "temperature":
                    self.temperature,

                "maxTokens":
                    self.max_tokens
            }
        )


        content = (
            response["output"]
            ["message"]
            ["content"]
        )


        text_parts = [
            block["text"]
            for block in content
            if "text" in block
        ]


        return "".join(
            text_parts
        ).strip()