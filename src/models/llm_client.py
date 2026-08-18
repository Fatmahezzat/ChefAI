import os

from httpx import Client

from langchain.chat_models import init_chat_model

MODEL_NAME = "gemini-3.6-flash"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
HTTP_CLIENT = Client()

def get_llm():
    return init_chat_model(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        model_provider="google_genai",
        max_tokens=2000,
        temperature=0.8,
        timeout=30.0,
        max_retries=3,
    )