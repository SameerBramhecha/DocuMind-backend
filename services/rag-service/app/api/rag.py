from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import requests
import json

from app.services.vector_search import VectorSearch
from app.services.llm_client import LLMClient
from app.config import settings

router = APIRouter()
vector_search = VectorSearch()
llm_client = LLMClient()

class QuestionRequest(BaseModel):
    question: str
    top_k: int = 5

class QuestionResponse(BaseModel):
    answer: str
    sources: List[dict]
    question: str

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question and get an answer using RAG"""
    try:
        # 1. Get embedding for the question
        embedding_response = requests.post(
            settings.EMBEDDING_SERVICE_URL,
            json={"text": request.question}
        )
        embedding_response.raise_for_status()
        question_embedding = embedding_response.json()["embedding"]
        
        # 2. Search for similar documents
        search_results = vector_search.search_similar(question_embedding, request.top_k)
        
        if not search_results:
            # Try to answer without context
            try:
                answer = llm_client.generate_response(request.question, "")
                return QuestionResponse(
                    answer=answer,
                    sources=[],
                    question=request.question
                )
            except Exception as e:
                return QuestionResponse(
                    answer="I couldn't find any relevant documents to answer your question, and I'm unable to generate a general response.",
                    sources=[],
                    question=request.question
                )
        
        # 3. Extract context from search results
        context = vector_search.get_context_from_results(search_results)
        
        # 4. Generate answer using LLM
        answer = llm_client.generate_response(request.question, context)
        
        # 5. Prepare sources
        sources = []
        for result in search_results:
            payload = result.get("payload", {})
            sources.append({
                "filename": payload.get("filename", "Unknown"),
                "chunk_index": payload.get("chunk_index", 0),
                "score": result.get("score", 0),
                "text_preview": payload.get("original_text", "")[:200] + "..."
            })
        
        return QuestionResponse(
            answer=answer,
            sources=sources,
            question=request.question
        )
        
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")

@router.post("/ask/stream")
async def ask_question_stream(request: QuestionRequest):
    """Ask a question and get a streaming answer using RAG"""
    try:
        # 1. Get embedding for the question
        embedding_response = requests.post(
            settings.EMBEDDING_SERVICE_URL,
            json={"text": request.question}
        )
        embedding_response.raise_for_status()
        question_embedding = embedding_response.json()["embedding"]
        
        # 2. Search for similar documents
        search_results = vector_search.search_similar(question_embedding, request.top_k)
        
        if not search_results:
            return StreamingResponse(
                iter([json.dumps({"error": "No relevant documents found"})]),
                media_type="application/json"
            )
        
        # 3. Extract context from search results
        context = vector_search.get_context_from_results(search_results)
        
        # 4. Generate streaming response
        def generate():
            try:
                for chunk in llm_client.generate_streaming_response(request.question, context):
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                yield f"data: {json.dumps({'done': True})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return StreamingResponse(generate(), media_type="text/plain")
        
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}") 