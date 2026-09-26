from fastapi import APIRouter, Depends

from app.backend.api.models import (
    ChatRequest,
    ChatResponse
)

from app.backend.api.dependencies import (
    get_rag_service
)

from app.backend.rag.service import (
    RAGService
)


router = APIRouter()


@router.post("/chat",response_model=ChatResponse)
def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(
        get_rag_service
    )
):
    return rag_service.ask(
        question=request.question,
        k=request.k
    )