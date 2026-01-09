# Smart Product Recommendation System

AI-powered product recommendation service using **OpenAI embeddings** and **FAISS** vector database with LLM-enhanced descriptions.

> ⚠️ Note: Generating LLM-based descriptions may take more than 2 seconds per request.

---

## Features

- ✅ **Semantic Search**: Understands user queries using OpenAI embeddings  
- ✅ **Fast Vector Search**: FAISS-based similarity search for sub-second response  
- ✅ **Explainable Recommendations**: Provides similarity scores  
- ✅ **RESTful API**: FastAPI backend with Swagger/OpenAPI docs  
- ✅ **Interactive UI**: Streamlit frontend for quick testing  
- ✅ **Production Ready**: Logging, error handling, and environment configuration  
- ✅ **LLM-enhanced Descriptions**: Generates creative product descriptions  

---

## Project Structure

smart-recommendation/
├── app/ # FastAPI backend
│ ├── init.py
│ ├── main.py # Entry point for FastAPI
│ ├── config.py # Application settings
│ ├── models.py # Pydantic models
│ └── services/ # Service layer
│ ├── init.py
│ ├── embedding_service.py # OpenAI embeddings wrapper
│ ├── vector_store.py # FAISS vector store
│ ├── product.py # Sample product data
│ └── recommendation_service.py # Core recommendation logic
├── data/
│ └── faiss_index/ # Saved FAISS index files
├── streamlit_app/ # Frontend UI
│ ├── init.py
│ └── app.py # Streamlit frontend app
├── tests/ # Test suite
│ ├── init.py
│ └── test_api.py # Example API tests
├── .env # Environment variables
├── .gitignore # Git ignore rules
├── README.md # This file
├── main.py # Optional script to run backend
└── pyproject.toml # Python project config



## Architecture

+-----------------+      POST      +-------------------+
|   Streamlit UI  |  ---------->   |   FastAPI Backend |
| (User enters    |                | (Receives query, |
|  search query)  |                |  generates        |
+-----------------+                |  embeddings)      |
                                   +---------+---------+
                                             |
                                             v
                                   +-------------------+
                                   |   FAISS Vector    |
                                   |   Search Top-k    |
                                   |   Products        |
                                   +---------+---------+
                                             |
                                             v
                                   +-------------------+
                                   |  OpenAI LLM       |
                                   |  Enhance product  |
                                   |  description      |
                                   +---------+---------+
                                             |
                                             v
                                   +-------------------+
                                   |  Build JSON       |
                                   |  Recommendation   |
                                   |  Response         |
                                   +---------+---------+
                                             |
                                             v
                                   +-------------------+
                                   |   Streamlit UI    |
                                   | Display results   |
                                   +-------------------+

