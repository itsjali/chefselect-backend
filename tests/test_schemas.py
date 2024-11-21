import pytest

from datetime import datetime
from marshmallow import ValidationError

from app.schemas import CreateIngredientSchema, CreateInstructionSchema, RecipeDetailsSchema, ExtendedRecipeDetailsSchema


def test_ingredient_schema_with_valid_data():
    ingredient = {"unit": "100g", "name": "Chicken"}

    ingredient_schema = CreateIngredientSchema()
    result = ingredient_schema.load(ingredient)
    
    assert result["unit"] == "100g"
    assert result["name"] == "Chicken"


def test_ingredient_schema_raises_validation_error_if_invalid_data():
    ingredient = {"unit": "100g"}

    ingredient_schema = CreateIngredientSchema()

    with pytest.raises(ValidationError):
        ingredient_schema.load(ingredient)


def test_instruction_schema_with_valid_data():
    instruction = {"step": 1, "description": "Cook the chicken"}

    instruction_schema = CreateInstructionSchema()
    result = instruction_schema.load(instruction)

    assert result["step"] == 1
    assert result["description"] == "Cook the chicken"


def test_instruction_schema_raises_validation_error_if_invalid_data():
    instruction = {"step": 1}

    instruction_schema = CreateInstructionSchema()

    with pytest.raises(ValidationError):
        instruction_schema.load(instruction)


def test_recipe_schema_with_valid_data():
    recipe = {
        "title": "Chicken Curry",
        "description": "Delicious chicken curry with rice",
        "ingredients": [
            {"unit": "100g", "name": "Chicken"},
            {"unit": "200g", "name": "Rice"}
        ],
        "instructions": ["Step 1", "Step 2"]
    }

    recipe_schema = RecipeDetailsSchema()
    result = recipe_schema.load(recipe)
    
    assert result["title"] == "Chicken Curry"
    assert result["description"] == "Delicious chicken curry with rice"
    assert len(result["ingredients"]) == 2
    assert result["ingredients"][0]["unit"] == "100g"
    assert result["ingredients"][0]["name"] == "Chicken"
    assert len(result["instructions"]) == 2
    assert result["instructions"][0] == "Step 1"


def test_recipe_schema_raises_validation_error_if_invalid_data():
    recipe = {
        "title": "Chicken Curry",
        "description": "Delicious chicken curry with rice",
        "ingredients": [
            {"unit": "100g", "name": "Chicken"},
            {"unit": "200g", "name": "Rice"}
        ]
    }

    recipe_schema = RecipeDetailsSchema()

    with pytest.raises(ValidationError):
        recipe_schema.load(recipe)


def test_extended_recipe_details_schema_with_valid_data(valid_recipe_data):
    today = datetime.now()
    extended_data = {
        "recipe_fields": [valid_recipe_data],
        "id": "1234",
        "created_at": today.isoformat(),
    }

    extended_schema = ExtendedRecipeDetailsSchema()

    result = extended_schema.load(extended_data)

    assert result["recipe_fields"] == extended_data["recipe_fields"]
    assert result["id"] == extended_data["id"]
    assert result["created_at"] == today


def test_extended_recipe_details_raises_validation_error_with_invalid_data(valid_recipe_data):
    extended_data = {
        "recipe_fields": [valid_recipe_data],
        "id": 1234,
    }

    recipe_fields = extended_data["recipe_fields"][0]
    recipe_fields["title"] = "fake title"
    recipe_fields["ingredients"] = {"unit": "200g"}
    recipe_fields.pop("instructions")

    extended_schema = ExtendedRecipeDetailsSchema()

    with pytest.raises(ValidationError):
        extended_schema.load(extended_data)
