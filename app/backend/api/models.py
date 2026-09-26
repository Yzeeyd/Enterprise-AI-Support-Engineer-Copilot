from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=2000
    )

    k: int = Field(
        default=5,
        ge=1,
        le=20
    )


class SourceResponse(BaseModel):
    id: int
    document_id: str
    filename: str
    chunk_ids: list[str]
    score: float | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceResponse]