"""Validation and normalization helpers for user-submitted data."""

import json
import re
from urllib.parse import urlparse

MAX_DESCRIPTION_LENGTH = 2_000
MAX_INSTRUCTIONS_LENGTH = 10_000
MAX_INGREDIENTS = 100
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def clean_text(value):
    return (value or "").strip()


def normalize_ingredients(value, limit=MAX_INGREDIENTS):
    """Return one-per-line or comma-separated ingredients as a clean list."""
    raw_value = (value or "").replace("\r", "")
    lines = [line.strip() for line in raw_value.split("\n") if line.strip()]
    if len(lines) > 1:
        # One item per line is authoritative, so ingredient names containing
        # commas (for example, "oil, divided") remain intact.
        ingredients = lines
    else:
        ingredients = [part.strip() for part in raw_value.split(",") if part.strip()]
    return ingredients if limit is None else ingredients[:limit]


def serialize_ingredients(items):
    """Store the structured ingredient list in the existing Text column."""
    return json.dumps(items, ensure_ascii=False)


def _valid_photo_url(value):
    if not value:
        return True
    if value.startswith("/static/"):
        return True
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_recipe_form(form):
    """Return cleaned recipe values and a list of validation errors."""
    name = clean_text(form.get("name"))
    description = clean_text(form.get("description"))
    all_ingredients = normalize_ingredients(form.get("ingredients"), limit=None)
    ingredients = all_ingredients[:MAX_INGREDIENTS]
    instructions = clean_text(form.get("instructions"))
    photo = clean_text(form.get("photo"))
    category_id_value = clean_text(form.get("category_id"))

    cleaned = {
        "name": name,
        "description": description or None,
        "ingredients": ingredients,
        "instructions": instructions or None,
        "photo": photo or None,
        "category_id": None,
    }
    errors = []

    if not name:
        errors.append("Recipe name is required.")
    elif len(name) > 120:
        errors.append("Recipe name must be 120 characters or fewer.")

    if len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append("Description must be 2,000 characters or fewer.")

    if not ingredients:
        errors.append("At least one ingredient is required.")
    elif len(all_ingredients) > MAX_INGREDIENTS:
        errors.append(f"A recipe may contain at most {MAX_INGREDIENTS} ingredients.")

    if not instructions:
        errors.append("Instructions are required.")
    elif len(instructions) > MAX_INSTRUCTIONS_LENGTH:
        errors.append("Instructions must be 10,000 characters or fewer.")

    if not category_id_value:
        errors.append("A category is required.")
    else:
        try:
            cleaned["category_id"] = int(category_id_value)
        except ValueError:
            errors.append("The selected category is invalid.")

    if not _valid_photo_url(photo):
        errors.append("Photo must be an HTTP(S) URL or an application static path.")

    return cleaned, errors


def validate_category_form(form):
    name = clean_text(form.get("name"))
    photo = clean_text(form.get("photo"))
    errors = []
    if not name:
        errors.append("Category name is required.")
    elif len(name) > 50:
        errors.append("Category name must be 50 characters or fewer.")
    if not _valid_photo_url(photo):
        errors.append("Category photo must be an HTTP(S) URL or an application static path.")
    return {"name": name, "photo": photo or None}, errors


def validate_recommendation_input(form):
    ingredients = clean_text(form.get("ingredients"))
    servings_value = clean_text(form.get("servings"))
    errors = []
    servings = None

    if not ingredients:
        errors.append("Enter at least one ingredient.")
    elif len(ingredients) > 1_000:
        errors.append("Ingredients must be 1,000 characters or fewer.")

    if servings_value:
        try:
            servings = int(servings_value)
        except ValueError:
            errors.append("Servings must be a whole number.")
        else:
            if not 1 <= servings <= 50:
                errors.append("Servings must be between 1 and 50.")

    return {"ingredients": ingredients, "servings": servings}, errors


def validate_auth_input(username, email, password):
    username = clean_text(username)
    email = clean_text(email).lower()
    password = password or ""
    errors = []

    if not 3 <= len(username) <= 50:
        errors.append("Username must be between 3 and 50 characters.")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", username):
        errors.append("Username may contain only letters, numbers, dots, underscores, and hyphens.")
    if not EMAIL_PATTERN.fullmatch(email):
        errors.append("Enter a valid email address.")
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")

    return {"username": username, "email": email, "password": password}, errors
