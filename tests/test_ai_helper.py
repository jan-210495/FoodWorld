import requests

from utils import ai_helper
from utils.ai_helper import parse_recipe_response


def test_ai_json_response_is_strictly_parsed():
    recipes = parse_recipe_response(
        "```json\n"
        '{"recipes": [{"title": "Soup", "ingredients": ["water"], "steps": ["Simmer"]}]}'
        "\n```"
    )
    assert recipes == [
        {
            "title": "Soup",
            "ingredients": ["water"],
            "steps": ["Simmer"],
            "photo": "/static/img/default_food.jpg",
        }
    ]


def test_malformed_ai_response_is_empty():
    assert parse_recipe_response("<script>alert(1)</script>") == []


def test_image_timeout_returns_local_fallback(monkeypatch):
    monkeypatch.setenv("PEXELS_API_KEY", "test-key")
    ai_helper._search_food_image.cache_clear()

    def timeout(*args, **kwargs):
        raise requests.Timeout()

    monkeypatch.setattr(ai_helper.requests, "get", timeout)
    assert ai_helper.get_food_image("soup") == "/static/img/default_food.jpg"
    ai_helper._search_food_image.cache_clear()
