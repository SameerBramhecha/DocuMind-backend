from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser import extract_text_from_pdf
from app.services.chunker import TextChunker
from app.services.embedding_client import EmbeddingClient
from app.config import settings
import uuid

router = APIRouter()
chunker = TextChunker()
embedding_client = EmbeddingClient()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    contents = await file.read()
    try:
        extracted_text = extract_text_from_pdf(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")
    
    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="No text extracted from PDF.")

    # Generate a unique document ID
    document_id = str(uuid.uuid4())
    
    # Chunk the text
    chunks = chunker.chunk_text(extracted_text)
    
    # Prepare metadata for each chunk
    metadata_list = []
    for chunk in chunks:
        metadata = {
            "document_id": document_id,
            "filename": file.filename,
            "chunk_index": chunk["index"],
            "total_chunks": len(chunks)
        }
        metadata_list.append(metadata)
    
    # Get embeddings for all chunks
    try:
        texts = [chunk["text"] for chunk in chunks]
        embeddings = embedding_client.get_embeddings_batch(texts)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Embedding service error: {str(e)}")
    
    return {
        "document_id": document_id,
        "filename": file.filename,
        "chunks_processed": len(chunks),
        "preview": extracted_text[:300],
        "sample_embedding": embeddings[0][:5] if embeddings else []
    }
