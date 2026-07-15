from utils.validation import (
    normalize_ingredients,
    serialize_ingredients,
    validate_auth_input,
    validate_recipe_form,
)


def test_recipe_input_is_structured_and_validated():
    values, errors = validate_recipe_form(
        {
            "name": " Pasta ",
            "description": "A quick meal",
            "ingredients": "pasta\ntomato\nsalt",
            "instructions": "Boil the pasta.\nServe hot.",
            "category_id": "2",
            "photo": "https://example.com/pasta.jpg",
        }
    )
    assert errors == []
    assert values["name"] == "Pasta"
    assert values["ingredients"] == ["pasta", "tomato", "salt"]
    assert values["category_id"] == 2
    assert serialize_ingredients(values["ingredients"]).startswith("[")


def test_invalid_auth_input_is_rejected():
    values, errors = validate_auth_input("x", "not-an-email", "short")
    assert values["email"] == "not-an-email"
    assert len(errors) == 3


def test_ingredient_names_with_commas_are_preserved_on_separate_lines():
    assert normalize_ingredients("rice\n chicken, divided") == ["rice", "chicken, divided"]


def test_legacy_comma_ingredient_input_is_supported():
    assert normalize_ingredients("rice, chicken, salt") == ["rice", "chicken", "salt"]
