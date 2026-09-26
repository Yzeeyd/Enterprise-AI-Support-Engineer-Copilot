from fastapi import FastAPI

from app.backend.api.routes import router


app = FastAPI(
    title="Enterprise AI Support Engineer Copilot",
    description=(
        "Enterprise support copilot powered "
        "by Hybrid RAG and OpenSearch"
    ),
    version="0.1.0"
)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


app.include_router(
    router,
    prefix="/api/v1"
)