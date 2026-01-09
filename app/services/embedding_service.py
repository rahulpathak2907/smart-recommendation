import openai
from typing import List
import numpy as np
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings using OpenAI"""
    
    def __init__(self):
        self.settings = get_settings()
        openai.api_key = self.settings.openai_api_key
        self.model = self.settings.embedding_model
        self.cache = {}
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Get embedding for a single text Uses caching to avoid redundant API calls"""

        cache_key = text.lower().strip()
        
        if cache_key in self.cache:
            logger.info(f"Cache hit for text: {text[:50]}...")
            return self.cache[cache_key]
        
        try:
            response = openai.embeddings.create(
                model=self.model,
                input=text
            )
            embedding = np.array(response.data[0].embedding, dtype=np.float32)
            self.cache[cache_key] = embedding
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def get_embeddings_batch(self, texts: List[str]) -> List[np.ndarray]:
        """Get embeddings for multiple texts More efficient than individual calls"""
    
        uncached_texts = []
        uncached_indices = []
        embeddings = [None] * len(texts)
        
        for i, text in enumerate(texts):
            cache_key = text.lower().strip()
            if cache_key in self.cache:
                embeddings[i] = self.cache[cache_key]
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)
        

        if uncached_texts:
            try:
                response = openai.embeddings.create(
                    model=self.model,
                    input=uncached_texts
                )
                
                for i, embedding_data in enumerate(response.data):
                    embedding = np.array(embedding_data.embedding, dtype=np.float32)
                    original_idx = uncached_indices[i]
                    embeddings[original_idx] = embedding
                    
                    cache_key = uncached_texts[i].lower().strip()
                    self.cache[cache_key] = embedding
                    
            except Exception as e:
                logger.error(f"Error generating batch embeddings: {str(e)}")
                raise
        
        return embeddings
    
    def clear_cache(self):
        """Clear the embedding cache"""
        self.cache.clear()