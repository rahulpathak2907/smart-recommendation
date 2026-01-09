# Smart Product Recommendation System

> **Note:** Generating descriptions using LLM calls may take more than 2 seconds per request.

## To Run
1.uvicorn app.main:app --reload
2.streamlit run streamlit_app/app.py

AI-powered product recommendation service leveraging **OpenAI embeddings** and **FAISS** vector database.

## Features

- ✅ **Semantic Search**: Understands user intent using OpenAI embeddings.
- ✅ **Fast Vector Search**: FAISS-based similarity search for efficient results.
- ✅ **Explainable AI**: Clear similarity scores and descriptive product explanations.
- ✅ **RESTful API**: Built with FastAPI and automatic documentation (`/docs`).
- ✅ **Interactive UI**: Streamlit frontend for easy product search testing.
- ✅ **Production Ready**: Includes logging, error handling, and caching.
- ✅ **LLM-Enhanced Descriptions**: Generates friendly, human-readable product descriptions.

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

