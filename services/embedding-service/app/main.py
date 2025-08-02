from fastapi import FastAPI
from app.api import embed

app = FastAPI(
    title="Embedding Service",
    version="1.0.0"
)

app.include_router(embed.router, prefix="/api")
