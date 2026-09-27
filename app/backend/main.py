from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from app.backend.api.routes import router


app = FastAPI(
    title="Enterprise AI Support Engineer Copilot",
    description=(
        "Enterprise support copilot powered "
        "by Hybrid RAG and OpenSearch"
    ),
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
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


# AWS Lambda entry point
handler = Mangum(
    app,
    lifespan="off"
)