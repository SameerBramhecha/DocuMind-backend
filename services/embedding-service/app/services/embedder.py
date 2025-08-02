from sentence_transformers import SentenceTransformer
from app.config import settings

class EmbedderService:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def get_embedding(self, text: str):
        return self.model.encode(text).tolist()
