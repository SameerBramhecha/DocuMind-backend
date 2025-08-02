import requests
from typing import List, Dict, Any
from app.config import settings

class EmbeddingClient:
    def __init__(self):
        self.base_url = settings.EMBEDDING_SERVICE_URL.replace("/api/embed", "")
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text from the embedding service"""
        response = requests.post(
            f"{self.base_url}/api/embed",
            json={"text": text},
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()["embedding"]
    
    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple texts"""
        embeddings = []
        for text in texts:
            embedding = self.get_embedding(text)
            embeddings.append(embedding)
        return embeddings 