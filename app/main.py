from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from app.models import SearchRequest, RecommendationResponse
from app.services.recommendation_service import RecommendationService
from app.config import get_settings


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Smart Product Recommendation API",
    description="AI-powered product recommendation service using OpenAI embeddings and FAISS",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings = get_settings()

recommendation_service = RecommendationService()


@app.get("/")
async def root():
    return {
        "message": "Smart Product Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "recommend": "/api/v1/recommend",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "recommendation-api"
    }


@app.post("/api/v1/recommend", response_model=RecommendationResponse)
async def recommend_products(request: SearchRequest):

    try:
        logger.info(f"Received recommendation request: '{request.query}'")

        if not request.query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query cannot be empty"
            )

        response = recommendation_service.get_recommendations(request.query)

        logger.info(f"Returned {len(response.recommendations)} recommendations")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
