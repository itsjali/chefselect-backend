import requests
import os

from datetime import datetime
from unittest import mock


####### CREATE RECIPE #######

def test_create_recipe_view_success(valid_recipe_data):
    app_url = os.getenv("FLASK_URL")
    url = f"{app_url}/create-recipe"
    
    response = requests.post(url, json=valid_recipe_data)

    assert response.status_code == 200


def test_create_recipe_view_failure_with_invalid_payload():
    payload = {
        "description": 12,
        "ingredients": "fake ingredients",
        "instructions": {"Step 1": "Step 2"},
    }
    
    app_url = os.getenv("FLASK_URL")
    url = f"{app_url}/create-recipe"
    
    response = requests.post(url, json=payload)

    response_data = response.json()
    error_msg = response_data["errors"]

    assert response.status_code == 400
    assert "Not a valid string." in error_msg["description"] 
    assert "Not a valid list." in error_msg["ingredients"]
    assert "Not a valid list." in error_msg["instructions"]
    assert "Missing data for required field." in error_msg["title"]


####### GET_RECIPES #######


def test_get_recipes_view_success():
    app_url = os.getenv("FLASK_URL")
    url = f"{app_url}/get-recipes"

    response = requests.post(url)

    assert response.status_code == 200
