"""Validation and normalization helpers for user-submitted recipe data."""

from urllib.parse import urlparse


MAX_DESCRIPTION_LENGTH = 2_000
MAX_INSTRUCTIONS_LENGTH = 10_000


def _text(value):
    return (value or "").strip()


def normalize_ingredients(value):
    """Normalize one-per-line or comma-separated ingredients for storage."""
    ingredients = []
    for line in (value or "").replace("\r", "").split("\n"):
        ingredients.extend(part.strip() for part in line.split(","))
    return ", ".join(item for item in ingredients if item)


def _valid_photo_url(value):
    """Allow remote HTTP(S) images and paths served by this application."""
    if not value:
        return True
    if value.startswith("/static/"):
        return True

    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_recipe_form(form):
    """Return cleaned recipe values and a list of validation errors."""
    name = _text(form.get("name"))
    description = _text(form.get("description"))
    ingredients = normalize_ingredients(form.get("ingredients"))
    instructions = _text(form.get("instructions"))
    photo = _text(form.get("photo"))
    category_id_value = _text(form.get("category_id"))

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
