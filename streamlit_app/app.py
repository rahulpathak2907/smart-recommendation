import streamlit as st
import requests

st.set_page_config(page_title="Smart Product Search", page_icon="🔍", layout="centered")

# API endpoint
API_URL = "http://localhost:8000/api/v1/recommend"

st.title("🔍 Smart Product Search")

query = st.text_input("Enter your search query", placeholder="e.g., red party dress")

if st.button("Search") and query.strip():
    with st.spinner("Finding best matches..."):
        try:
            response = requests.post(API_URL, json={"query": query}, timeout=10)
            response.raise_for_status()
            result = response.json()

            recommendations = result.get("recommendations", [])
            processing_time = result.get("processing_time_ms", 0)

            if recommendations:
                st.success(f"Found {len(recommendations)} recommendations in {processing_time:.2f} ms")
                
                for idx, rec in enumerate(recommendations, 1):
                    product = rec["product"]
                    score = rec["score"]

                    st.markdown(f"### {idx}. {product['title']}")
                    st.markdown(f"**Tags:** {', '.join(product.get('tags', []))}")
                    st.markdown(f"**Similarity Score:** {score['similarity_score']:.2%}")
                    st.markdown(f"**Description:** {product.get('description', '')}")
                    st.divider()
            else:
                st.info("No recommendations found.")

        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {str(e)}")
