from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.services.embedder import EmbedderService
from app.services.qdrant import add_embedding_to_qdrant

router = APIRouter()
embedder = EmbedderService()

class TextRequest(BaseModel):
    text: str
    metadata: Optional[dict] = None

class BatchTextRequest(BaseModel):
    texts: List[str]
    metadata_list: Optional[List[dict]] = None

class EmbeddingResponse(BaseModel):
    embedding: list[float]

class BatchEmbeddingResponse(BaseModel):
    embeddings: List[list[float]]

@router.post("/embed", response_model=EmbeddingResponse)
def embed_text(request: TextRequest):
    embedding = embedder.get_embedding(request.text)
    
    # Save to qdrant with metadata
    metadata = request.metadata or {}
    metadata.update({
        "source": "api_embed",
        "original_text": request.text[:300]  # keep metadata size manageable
    })
    
    add_embedding_to_qdrant(embedding, metadata)
    return {"embedding": embedding}

@router.post("/embed/batch", response_model=BatchEmbeddingResponse)
def embed_texts_batch(request: BatchTextRequest):
    embeddings = []
    
    for i, text in enumerate(request.texts):
        embedding = embedder.get_embedding(text)
        embeddings.append(embedding)
        
        # Save to qdrant with metadata
        metadata = request.metadata_list[i] if request.metadata_list and i < len(request.metadata_list) else {}
        metadata.update({
            "source": "api_embed_batch",
            "original_text": text[:300],
            "batch_index": i
        })
        
        add_embedding_to_qdrant(embedding, metadata)
    
    return {"embeddings": embeddings}
