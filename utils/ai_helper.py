# utils/ai_helper.py

import os
import google.generativeai as genai
import requests
import re
import html
from bs4 import BeautifulSoup

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


def query_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    return response.text


def get_food_image(query):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            return data["photos"][0]["src"]["medium"]
    return "/static/img/default_food.jpg"


def convert_lists_to_checkboxes(soup):
    # Convert ingredients <ul> to checkboxes
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

    # Convert steps <ol> to checkboxes
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
