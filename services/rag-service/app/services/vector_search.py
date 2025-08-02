from qdrant_client import QdrantClient
from typing import List, Dict, Any
from app.config import settings

class VectorSearch:
    def __init__(self):
        self.client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        self.collection_name = "document_embeddings"
    
    def search_similar(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents in Qdrant"""
        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k
            )
            
            return [
                {
                    "score": result.score,
                    "payload": result.payload,
                    "id": result.id
                }
                for result in search_results
            ]
        except Exception as e:
            print(f"Error searching Qdrant: {e}")
            return []
    
    def get_context_from_results(self, search_results: List[Dict[str, Any]]) -> str:
        """Extract context from search results for LLM prompt"""
        context_parts = []
        
        for i, result in enumerate(search_results, 1):
            payload = result.get("payload", {})
            original_text = payload.get("original_text", "")
            filename = payload.get("filename", "Unknown")
            chunk_index = payload.get("chunk_index", 0)
            
            context_parts.append(f"Document {i} (from {filename}, chunk {chunk_index}):\n{original_text}\n")
        
        return "\n".join(context_parts) 