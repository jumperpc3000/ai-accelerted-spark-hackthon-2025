import streamlit as st
import requests
import os

# Set up Streamlit UI
st.set_page_config(page_title="AI Accelerated Tutor", page_icon="🤖")
st.title("🚀 AI Accelerated Spark Tutor")
st.markdown("Ask me anything about RAPIDS, GPU acceleration, Sol, or LLMs!")

# Sidebar controls
model = st.sidebar.selectbox("Choose a model", [
    ("OpenAI - GPT-4o", "openai", "gpt4o"),
    ("Anthropic - Claude 3 Haiku", "anthropic", "claude3_haiku"),
    ("Mistral - Mixtral 8x7B", "mistral", "mixtral_8x7b"),
    ("Google - Gemini 1.5 Flash", "google", "gemini_1_5_flash")
])

# User query
user_input = st.text_input("🔍 Ask your question:")

if st.button("Submit") and user_input:
    api_url = "https://api-main-beta.aiml.asu.edu/query"
    api_key = st.secrets["API_KEY"]  # Stored in Streamlit secrets

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "action": "query",
        "request_source": "override_params",
        "query": user_input,
        "model_provider": model[1],
        "model_name": model[2],
        "enable_search": True,
        "search_params": {
            "collection": "1f6d1cd1458a41a49648b7a7aea5c5d4",
            "top_k": 3,
            "retrieval_type": "chunk",
            "output_fields": ["content", "source_name"]
        },
        "response_format": {"type": "json"}
    }

    with st.spinner("Thinking..."):
        try:
            response = requests.post(api_url, headers=headers, json=payload)
            data = response.json()
            if "response" in data:
                st.success("Response:")
                st.write(data["response"])
                if "metadata" in data and "sources" in data["metadata"]:
                    st.markdown("---")
                    st.caption("📚 Sources:")
                    for src in data["metadata"]["sources"]:
                        st.write(f"- {src['source_name']}")
            else:
                st.error("No response returned. Check your input or model settings.")
        except Exception as e:
            st.error(f"Request failed: {e}")
