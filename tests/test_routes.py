from models import db
from models.category import Category
from models.recipe import Recipe
from models.user import User
from tests.conftest import login


def test_public_home_and_missing_route_are_safe(client):
    response = client.get("/user/")
    assert response.status_code == 200
    assert client.get("/user/canva").status_code == 404


def test_registration_and_login(client, app):
    response = client.post(
        "/user/register",
        data={
            "username": "homechef",
            "email": "chef@example.com",
            "password": "correct horse battery staple",
        },
    )
    assert response.status_code == 302
    with app.app_context():
        assert User.query.filter_by(email="chef@example.com").first() is not None
    response = login(client, "chef@example.com")
    assert response.status_code == 302
    assert "/user/home" in response.headers["Location"]
    assert client.post("/user/logout").status_code == 302


def test_customer_cannot_access_admin_dashboard(client):
    response = client.post(
        "/user/register",
        data={
            "username": "customer",
            "email": "customer@example.com",
            "password": "correct horse battery staple",
        },
    )
    assert response.status_code == 302
    login(client, "customer@example.com")
    assert client.get("/recipes/dashboard").status_code == 403
    assert client.get("/recipes/categories/manage").status_code == 403


def test_recipe_crud_requires_admin_and_uses_category(client, app, admin, category):
    response = client.get("/recipes/add")
    assert response.status_code == 302
    assert "/user/login" in response.headers["Location"]

    with app.app_context():
        email = db.session.get(User, admin).email
    login(client, email)

    response = client.post(
        "/recipes/add",
        data={
            "name": "Tomato Pasta",
            "ingredients": "pasta\ntomato\nsalt",
            "instructions": "Boil pasta.\nAdd sauce.",
            "category_id": str(category),
            "photo": "",
        },
        follow_redirects=False,
    )
    assert response.status_code == 302

    with app.app_context():
        recipe = Recipe.query.filter_by(name="Tomato Pasta").one()
        assert recipe.ingredient_items == ["pasta", "tomato", "salt"]
        recipe_id = recipe.id

    response = client.post(
        f"/recipes/edit/{recipe_id}",
        data={
            "name": "Updated Pasta",
            "ingredients": "pasta\ntomato",
            "instructions": "Cook and serve.",
            "category_id": str(category),
            "photo": "",
        },
    )
    assert response.status_code == 302

    with app.app_context():
        assert db.session.get(Recipe, recipe_id).name == "Updated Pasta"


def test_search_favorite_and_category_pages(client, app, admin, category):
    with app.app_context():
        recipe = Recipe(
            name="Saved Soup",
            ingredients='["water", "vegetables"]',
            instructions="Simmer.",
            category_id=category,
        )
        db.session.add(recipe)
        db.session.commit()
        recipe_id = recipe.id
        email = db.session.get(User, admin).email

    assert client.get("/recipes/search?q=soup").status_code == 200
    assert client.get("/recipes/categories").status_code == 200
    assert client.get(f"/recipes/category/{category}").status_code == 200
    login(client, email)
    assert client.get("/recipes/categories/manage").status_code == 200
    response = client.post(f"/recipes/{recipe_id}/favorite")
    assert response.status_code == 302

    with app.app_context():
        assert len(db.session.get(Recipe, recipe_id).favorites) == 1


def test_admin_can_manage_categories(client, app, admin):
    with app.app_context():
        email = db.session.get(User, admin).email
    login(client, email)
    response = client.post("/recipes/categories/add", data={"name": "Breakfast", "photo": ""})
    assert response.status_code == 302
    with app.app_context():
        category = Category.query.filter_by(name="Breakfast").one()
        category_id = category.id
    response = client.post(
        f"/recipes/categories/edit/{category_id}",
        data={"name": "Brunch", "photo": ""},
    )
    assert response.status_code == 302
    response = client.post(f"/recipes/categories/delete/{category_id}")
    assert response.status_code == 302
