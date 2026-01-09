from pydantic import BaseModel, Field
from typing import List, Optional


class Product(BaseModel):
    """Product model"""
    id: int
    title: str
    tags: List[str] = Field(default_factory=list)
    description: Optional[str] = None


class SearchRequest(BaseModel):
    """Search request model"""
    query: str 



class RecommendationExplanation(BaseModel):
    """Explanation for a recommendation"""
    similarity_score: float = Field(..., ge=0, le=1)


class ProductRecommendation(BaseModel):
    """Single product recommendation"""
    product: Product
    score: RecommendationExplanation


class RecommendationResponse(BaseModel):
    """API response model"""
    query: str
    recommendations: List[ProductRecommendation]
    processing_time_ms: float