from marshmallow import Schema, fields


class CreateIngredientSchema(Schema):
    unit = fields.String(required=True)
    name = fields.String(required=True)


class CreateInstructionSchema(Schema):
    step = fields.Integer(required=True)
    description = fields.String(required=True)


class RecipeDetailsSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    ingredients = fields.List(fields.Nested(CreateIngredientSchema), required=True)
    instructions = fields.List(fields.String(), required=True)


class ExtendedRecipeDetailsSchema(Schema):
    recipe_fields = fields.List(fields.Nested(RecipeDetailsSchema), required=True)
    id = fields.String(required=True)
    created_at = fields.DateTime(required=True)
