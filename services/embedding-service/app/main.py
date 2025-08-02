from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import embed
from app.api import search

app = FastAPI(
    title="Embedding Service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(embed.router, prefix="/api")
app.include_router(search.router, prefix="/api")