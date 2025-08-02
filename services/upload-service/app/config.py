import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    EMBEDDING_SERVICE_URL: str = os.getenv("EMBEDDING_SERVICE_URL", "http://localhost:8002/embed")
    
settings = Settings()