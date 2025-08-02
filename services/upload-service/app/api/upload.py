from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser import extract_text_from_pdf
from app.config import settings  # 👈 import your config
import requests

router = APIRouter()

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

    try:
        response = requests.post(
            settings.EMBEDDING_SERVICE_URL,
            json={"text": extracted_text}
        )
        response.raise_for_status()
        embedding = response.json().get("embedding", [])
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Embedding service error: {str(e)}")
    
    return {
        "filename": file.filename,
        "preview": extracted_text[:300],
        "embedding": embedding[:5]
    }
