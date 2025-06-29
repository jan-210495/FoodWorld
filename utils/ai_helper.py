import requests
import os

HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_API_KEY = "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"

def generate_recipe(ingredients, servings):
    prompt = (
        f"Write a detailed recipe using these ingredients: {ingredients}. "
        f"The recipe should serve {servings} people. "
        "Include ingredients list and instructions."
    )

    payload = {
        "inputs": prompt,
        "options": {
            "max_length": 300,
            "do_sample": True,
            "temperature": 0.7,
        }
    }

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    response = requests.post(HF_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"]
    else:
        print("❌ Hugging Face API error:", response.text)
        return None
