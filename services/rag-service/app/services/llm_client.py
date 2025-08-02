import requests
from typing import Dict, Any
from app.config import settings

class LLMClient:
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.LLM_MODEL
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate response using Ollama LLM"""
        try:
            # Create a RAG prompt with context
            full_prompt = self._create_rag_prompt(prompt, context)
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=60.0  # Reduced timeout
            )
            response.raise_for_status()
            
            return response.json().get("response", "Sorry, I couldn't generate a response.")
            
        except requests.RequestException as e:
            print(f"Error calling Ollama: {e}")
            return f"Error: Could not connect to LLM service. {str(e)}"
    
    def _create_rag_prompt(self, question: str, context: str) -> str:
        """Create a RAG prompt with context"""
        if context:
            return f"""Based on the following context, please answer the question. If the context doesn't contain enough information to answer the question, say so.

Context:
{context}

Question: {question}

Answer:"""
        else:
            return f"""Please answer the following question: {question}"""
    
    def generate_streaming_response(self, prompt: str, context: str = ""):
        """Generate streaming response using Ollama"""
        try:
            full_prompt = self._create_rag_prompt(prompt, context)
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "stream": True
                },
                stream=True,
                timeout=60.0
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        data = requests.utils.json.loads(line)
                        if "response" in data:
                            yield data["response"]
                        if data.get("done", False):
                            break
                    except:
                        continue
                        
        except requests.RequestException as e:
            yield f"Error: Could not connect to LLM service. {str(e)}" 