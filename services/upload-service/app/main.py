from fastapi import FastAPI
from app.api.upload import router as upload_router

app = FastAPI(title="Upload Service", version="1.0")

app.include_router(upload_router, prefix="/upload", tags=["Upload"])