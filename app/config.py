from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    openai_api_key: str
    text_model:str
    embedding_model: str = "text-embedding-3-small"
    faiss_index_path: str = "./data/faiss_index"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    max_recommendations: int = 3
    embedding_dimension: int = 1536
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()