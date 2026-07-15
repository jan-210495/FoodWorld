import pytest

from app import create_app
from config import TestingConfig
from models import db
from models.category import Category
from models.user import User


@pytest.fixture()
def app():
    application = create_app(TestingConfig)
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def admin(app):
    with app.app_context():
        user = User(username="admin", email="admin@example.com", role="admin", confirmed=True)
        user.set_password("correct horse battery staple")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture()
def category(app):
    with app.app_context():
        item = Category(name="Dinner", photo=None)
        db.session.add(item)
        db.session.commit()
        return item.id


def login(client, email, password="correct horse battery staple"):
    return client.post(
        "/user/login",
        data={"email": email, "password": password},
        follow_redirects=False,
    )
