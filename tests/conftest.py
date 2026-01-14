import os
import pytest
import requests

from app import create_app
from app.models import db
from app.config import TestConfig


DEV_USER_EMAIL = os.getenv("DEV_USER_EMAIL")
DEV_USER_PASSWORD = os.getenv("DEV_USER_PASSWORD")
FLASK_URL = os.getenv("FLASK_URL")


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app(config_class="app.config.TestConfig")

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


@pytest.fixture(scope="module")
def init_database():
    flask_app = create_app(TestConfig)

    with flask_app.app_context():
        db.create_all()
        yield db
        db.drop_all()


@pytest.fixture(scope="session")
def access_token():
    request = requests.post(
        f"{FLASK_URL}/login",
        json={"email": DEV_USER_EMAIL, "password": DEV_USER_PASSWORD},
    )
    assert request.status_code == 200
    return request.json()["access_token"]


@pytest.fixture
def auth_headers(access_token):
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }


@pytest.fixture
def valid_recipe_data():
    title = "Pancakes"
    description = "Some simple pancakes"
    ingredients = [
        {"unit": "200g", "name": "Flour"},
    ]
    instructions = ["Mix ingredients"]

    return {
            "title": title,
            "description": description,
            "ingredients": ingredients,
            "instructions": instructions,
    }