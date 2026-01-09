from typing import List
import time
import os
import logging
from openai import OpenAI

from app.models import (
    Product, RecommendationResponse,
    ProductRecommendation, RecommendationExplanation
)
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.config import get_settings
from app.services.product import SAMPLE_PRODUCTS
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
TEXT_MODEL = os.getenv("TEXT_MODEL")

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service for generating product recommendations with LLM-enhanced descriptions"""

    def __init__(self):
        self.settings = get_settings()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.llm = OpenAI(api_key=API_KEY)
        self.products: List[Product] = [Product(**p) for p in SAMPLE_PRODUCTS]
        self._build_index_once()

    def _prepare_product_text(self, product: Product) -> str:
        parts = [product.title]
        if product.tags:
            parts.append(" ".join(product.tags))
        if product.description:
            parts.append(product.description)
        return " ".join(parts)

    def _build_index_once(self):
        logger.info("Building FAISS index once at startup...")

        product_texts = [
            self._prepare_product_text(p)
            for p in self.products
        ]

        embeddings = self.embedding_service.get_embeddings_batch(product_texts)

        metadata = [
            {"product": product}
            for product in self.products
        ]

        self.vector_store.add_vectors(embeddings, metadata)

        logger.info("FAISS index ready and kept in memory")

    def _enhance_description_with_llm(self, product: Product, query: str, score: float) -> str:
        """Generate 3 different friendly sentences for the product description and return them as a single string"""

        prompt = f"""
        You are a creative shopping assistant.

        User searched: "{query}"

        Product:
        Title: {product.title}
        Tags: {', '.join(product.tags)}
        Original description: {product.description or ''}

        Generate 3 different short, friendly sentences explaining why this product is a great fit.
        Each sentence should be unique, natural, and appealing. Return each sentence on a new line.
        """

        try:
            res = self.llm.chat.completions.create(
                model= TEXT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=50
            )

            text = res.choices[0].message.content.strip()
            lines = [line.strip() for line in text.split("\n") if line.strip()]

            while len(lines) < 3:
                lines.append(lines[-1] if lines else "A great product matching your search.")

            return " ".join(lines[:3])

        except Exception as e:
            logger.error(f"LLM description enhancement failed: {e}")
            fallback = product.description or "A great product matching your search."
            return fallback

    def get_recommendations(self, query: str) -> RecommendationResponse:
        start_time = time.time()

        try:
            logger.info(f"Processing query: {query}")

            query_embedding = self.embedding_service.get_embedding(query)

            k = min(self.settings.max_recommendations, len(self.products))
            results = self.vector_store.search(query_embedding, k=k)

            recommendations = []
            for metadata, score_value in results:
                product = metadata["product"]

                product.description = self._enhance_description_with_llm(product, query, score_value)

                score = RecommendationExplanation(similarity_score=round(score_value, 4))

                recommendations.append(
                    ProductRecommendation(
                        product=product,
                        score=score
                    )
                )

            processing_time = (time.time() - start_time) * 1000
            logger.info(f"Generated {len(recommendations)} recommendations in {processing_time:.2f}ms")

            return RecommendationResponse(
                query=query,
                recommendations=recommendations,
                processing_time_ms=round(processing_time, 2)
            )

        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}", exc_info=True)
            raise
