from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embedder import EmbedderService
from app.services.qdrant import add_embedding_to_qdrant

router = APIRouter()
embedder = EmbedderService()

class TextRequest(BaseModel):
    text: str

class EmbeddingResponse(BaseModel):
    embedding: list[float]

@router.post("/embed", response_model=EmbeddingResponse)
def embed_text(request: TextRequest):
    embedding = embedder.get_embedding(request.text)
    
    #save to qdrant with minimal metadata
    metadata = {
        "source" : "api_embed",
        "original_text" : request.text[:300] #keep metadata size manageable
    }
    
    add_embedding_to_qdrant(embedding,metadata)
    return {"embedding": embedding}
