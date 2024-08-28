from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.schemas import RecipeSchema
from app.services import create_recipe_service, build_recipe_list

main_bp = Blueprint("main", __name__)


@main_bp.route("/create-recipe", methods=["POST"])
def create_recipe():
    """
    Endpoint that receives data from the frontend 
    """
    data = request.get_json()
    try:
        schema = RecipeSchema()
        validated_data = schema.load(data)

        recipe = create_recipe_service(validated_data)

        return jsonify({"message": "Success", "data": recipe.title}), 200
    
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400


@main_bp.route("/get-recipes", methods=["GET"])
def get_recipes():
    recipe_list = build_recipe_list()
    return jsonify(recipe_list)
