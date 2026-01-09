import faiss
import numpy as np
import os
import pickle
from typing import List, Tuple
from app.config import get_settings
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    """FAISS-based vector store for efficient similarity search"""
    
    def __init__(self):
        self.settings = get_settings()
        self.dimension = self.settings.embedding_dimension
        self.index = None
        self.metadata = []
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize FAISS index"""
        self.index = faiss.IndexFlatIP(self.dimension)
        logger.info(f"Initialized FAISS index with dimension {self.dimension}")
    
    def add_vectors(self, embeddings: List[np.ndarray], metadata: List[dict]):
        """
        Add vectors to the index
        
        Args:
            embeddings: List of embedding vectors
            metadata: List of metadata dicts (e.g., product info)
        """
        if len(embeddings) != len(metadata):
            raise ValueError("Embeddings and metadata must have same length")
        
        embeddings_array = np.array(embeddings, dtype=np.float32)
        faiss.normalize_L2(embeddings_array)
        
        self.index.add(embeddings_array)
        self.metadata.extend(metadata)
        
        logger.info(f"Added {len(embeddings)} vectors to index")
    
    def search(self, query_embedding: np.ndarray, k: int = 3) -> List[Tuple[dict, float]]:
        """
        Search for k nearest neighbors
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
            
        Returns:
            List of (metadata, similarity_score) tuples
        """
        query_embedding = query_embedding.reshape(1, -1).astype(np.float32)
        faiss.normalize_L2(query_embedding)
        
        k = min(k, self.index.ntotal)  
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx, score in zip(indices[0], distances[0]):
            if idx < len(self.metadata):  
                results.append((self.metadata[idx], float(score)))
        
        return results
    
    def clear(self):
        """Clear the index and metadata"""
        self._initialize_index()
        self.metadata = []
        logger.info("Cleared vector store")
    
    def save(self, path: str):
        """Save index and metadata to disk"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        faiss.write_index(self.index, f"{path}.index")
        
        with open(f"{path}.metadata", "wb") as f:
            pickle.dump(self.metadata, f)
        
        logger.info(f"Saved vector store to {path}")
    
    def load(self, path: str):
        """Load index and metadata from disk"""
        self.index = faiss.read_index(f"{path}.index")
        
        with open(f"{path}.metadata", "rb") as f:
            self.metadata = pickle.load(f)
        
        logger.info(f"Loaded vector store from {path}")