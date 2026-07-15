"""Helpers for optional AI and image-search integrations."""

import json
import os
import re
from functools import lru_cache

import google.generativeai as genai
import requests
from flask import current_app

DEFAULT_FOOD_IMAGE = "/static/img/default_food.jpg"


def _setting(name):
    """Read settings at call time instead of capturing secrets at import time."""
    try:
        return current_app.config.get(name)
    except RuntimeError:
        return os.getenv(name)


def query_gemini(prompt):
    """Generate text, returning None when the optional service is unavailable."""
    api_key = _setting("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text if response and response.text else None
    except Exception:
        return None


def _strip_json_fence(value):
    value = value.strip()
    value = re.sub(r"^```(?:json)?\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s*```$", "", value)
    return value.strip()


def parse_recipe_response(value):
    """Validate a model response into a small, renderable recipe structure."""
    if not value:
        return []

    try:
        parsed = json.loads(_strip_json_fence(value))
    except (TypeError, json.JSONDecodeError):
        return []

    if isinstance(parsed, dict):
        parsed = parsed.get("recipes", [])
    if not isinstance(parsed, list):
        return []

    recipes = []
    for item in parsed[:3]:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()[:120]
        ingredients = item.get("ingredients", [])
        steps = item.get("steps", [])
        if not title or not isinstance(ingredients, list) or not isinstance(steps, list):
            continue
        ingredients = [str(value).strip() for value in ingredients[:30] if str(value).strip()]
        steps = [str(value).strip() for value in steps[:30] if str(value).strip()]
        if ingredients and steps:
            recipes.append(
                {
                    "title": title,
                    "ingredients": ingredients,
                    "steps": steps,
                    "photo": DEFAULT_FOOD_IMAGE,
                }
            )
    return recipes


@lru_cache(maxsize=128)
def _search_food_image(query, api_key):
    try:
        response = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": api_key},
            params={"query": query, "per_page": 1},
            timeout=10,
        )
        response.raise_for_status()
        photos = response.json().get("photos", [])
        if photos:
            return photos[0].get("src", {}).get("medium", DEFAULT_FOOD_IMAGE)
    except (requests.RequestException, ValueError, AttributeError):
        pass
    return DEFAULT_FOOD_IMAGE


def get_food_image(query):
    """Return a cached Pexels image URL or a local fallback image."""
    api_key = _setting("PEXELS_API_KEY")
    if not api_key:
        return DEFAULT_FOOD_IMAGE
    return _search_food_image(str(query).strip()[:120], api_key)
