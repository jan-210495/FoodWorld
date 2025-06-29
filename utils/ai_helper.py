import requests
import os

HF_API_URL = "https://api-inference.huggingface.co/models/simonneupane/controlled-food-recipe-generation"

HF_TOKEN = os.getenv("HF_TOKEN")

def query_huggingface(prompt: str):
    """
    Send a text prompt to the Hugging Face Inference API
    and return the generated text.
    """
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }
    payload = {
        "inputs": prompt
    }
    try:
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return data[0]["generated_text"] if data else None
    except requests.RequestException as e:
        print(f"❌ Hugging Face API error: {e}")
        return None
