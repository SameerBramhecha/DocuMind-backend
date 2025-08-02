from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

client = QdrantClient(host="qdrant", port=6333)

COLLECTION_NAME = "document_embeddings"

def create_collection_if_not_exists():
    if not client.collection_exists(COLLECTION_NAME):
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance = Distance.COSINE)
        )
        
        
def add_embedding_to_qdrant(embedding: list[float], metadata: dict):
    create_collection_if_not_exists()
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload=metadata
    )
    
    client.upsert(
        collection_name = COLLECTION_NAME,
        points=[point]
    )