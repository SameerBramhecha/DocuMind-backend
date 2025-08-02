import re
from typing import List, Dict, Any

class TextChunker:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks"""
        # Clean the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        if len(text) <= self.chunk_size:
            return [{"text": text, "index": 0}]
        
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # If this isn't the last chunk, try to break at a sentence boundary
            if end < len(text):
                # Look for sentence endings within the last 100 characters
                search_start = max(start + self.chunk_size - 100, start)
                sentence_end = text.rfind('.', search_start, end)
                if sentence_end > start + self.chunk_size // 2:  # Only break if we find a reasonable sentence boundary
                    end = sentence_end + 1
            
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "index": chunk_index
                })
                chunk_index += 1
            
            # Move start position, accounting for overlap
            start = end - self.overlap
            if start >= len(text):
                break
        
        return chunks 