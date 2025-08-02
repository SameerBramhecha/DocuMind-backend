from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embedder import EmbedderService
from app.services.qdrant import search_similar_documents

router = APIRouter()
embedder = EmbedderService()

class SearchRequest(BaseModel):
    query: str
    top_k : int = 3
    
@router.post("/search")
def seamntic_search(request: SearchRequest):
    query_embedding = embedder.get_embedding(request.query)
    results = search_similar_documents(query_embedding, request.top_k)
    return results