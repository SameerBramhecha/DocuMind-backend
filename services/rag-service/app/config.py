import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    EMBEDDING_SERVICE_URL: str = os.getenv("EMBEDDING_SERVICE_URL", "http://embedding-service:8003/api/embed")
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "qdrant")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama2")  # For Ollama
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

settings = Settings() 