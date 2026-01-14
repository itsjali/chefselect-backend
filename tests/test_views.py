import requests
import os

FLASK_URL = os.getenv("FLASK_URL")


####### CREATE RECIPE #######


def test_create_recipe_view_success(auth_headers, valid_recipe_data):
    url = f"{FLASK_URL}/create-recipe"    
    response = requests.post(url, json=valid_recipe_data, headers=auth_headers)
    assert response.status_code == 200

def test_create_recipe_view_failure_with_invalid_payload(auth_headers):
    payload = {
        "description": 12,
        "ingredients": "fake ingredients",
        "instructions": {"Step 1": "Step 2"},
    }
    
    url = f"{FLASK_URL}/create-recipe"
    response = requests.post(url, json=payload, headers=auth_headers)
    response_data = response.json()
    
    error_msg = response_data["errors"]
    assert response.status_code == 400
    assert "Not a valid string." in error_msg["description"] 
    assert "Not a valid list." in error_msg["ingredients"]
    assert "Not a valid list." in error_msg["instructions"]
    assert "Missing data for required field." in error_msg["title"]


####### GET_RECIPES #######


def test_get_recipes_view_success(auth_headers):
    url = f"{FLASK_URL}/get-recipes"
    response = requests.get(url, headers=auth_headers)
    assert response.status_code == 200
