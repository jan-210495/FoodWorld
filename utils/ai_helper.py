"""Helpers for optional AI and image-search integrations."""

import os

import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from flask import current_app


DEFAULT_FOOD_IMAGE = "/static/img/default_food.jpg"


def _setting(name):
    """Read a setting at call time instead of capturing secrets at import time."""
    try:
        return current_app.config.get(name)
    except RuntimeError:
        # This fallback keeps the helper usable in isolated tests or scripts
        # that do not run inside a Flask application context.
        return os.getenv(name)


def query_gemini(prompt):
    """Generate a response, returning None when the optional service is absent."""
    api_key = _setting("GEMINI_API_KEY")
    if not api_key:
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text if response and response.text else None
    except Exception:
        # The caller can provide a user-facing fallback. Do not expose API
        # configuration or provider details in the response.
        return None


def get_food_image(query):
    """Return a Pexels image URL or a local fallback image."""
    api_key = _setting("PEXELS_API_KEY")
    if not api_key:
        return DEFAULT_FOOD_IMAGE

    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": 1}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        photos = data.get("photos", [])
        if photos:
            return photos[0].get("src", {}).get("medium", DEFAULT_FOOD_IMAGE)
    except (requests.RequestException, ValueError, AttributeError):
        pass

    return DEFAULT_FOOD_IMAGE


def convert_lists_to_checkboxes(soup):
    """Convert generated ingredient and instruction lists into checkboxes."""
    for ul in soup.find_all("ul"):
        new_div = soup.new_tag("div", **{"class": "checkbox-list"})
        for li in ul.find_all("li"):
            label = soup.new_tag("label", **{"class": "checkbox-item"})
            checkbox = soup.new_tag("input", type="checkbox")
            span = soup.new_tag("span")
            span.string = li.get_text(strip=True)
            label.append(checkbox)
            label.append(span)
            new_div.append(label)
        ul.replace_with(new_div)

    for ol in soup.find_all("ol"):
        new_div = soup.new_tag("div", **{"class": "checkbox-list"})
        for li in ol.find_all("li"):
            label = soup.new_tag("label", **{"class": "checkbox-item"})
            checkbox = soup.new_tag("input", type="checkbox")
            span = soup.new_tag("span")
            span.string = li.get_text(strip=True)
            label.append(checkbox)
            label.append(span)
            new_div.append(label)
        ol.replace_with(new_div)

    return soup
