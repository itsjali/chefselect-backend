from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr


db = SQLAlchemy()
Column = db.Column


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(db.DateTime, default=datetime.now(), nullable=False)
    
    @declared_attr
    def updated_at(cls):
        return Column(db.DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class User(UserMixin, TimestampMixin, db.Model):
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(20), nullable=False)
    email = Column(db.String(100), unique=True, nullable=False)
    password = Column(db.String(100), nullable=False)


class Recipe(TimestampMixin, db.Model):
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(200), nullable=False)
    description = Column(db.String(1000), nullable=False)
    ingredients = db.relationship("Ingredient", backref="recipe", lazy=True, cascade="all, delete-orphan")
    instructions = db.relationship("Instruction", backref="recipe", lazy=True, cascade="all, delete-orphan")


class Ingredient(TimestampMixin, db.Model):
    id = Column(db.Integer, primary_key=True)
    unit = Column(db.String(50), nullable=False)
    name = Column(db.String(100), nullable=False)
    recipe_id = Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)


class Instruction(TimestampMixin, db.Model):
    id = Column(db.Integer, primary_key=True)
    step = Column(db.Integer, nullable=False)
    description = Column(db.Text, nullable=False)
    recipe_id = Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)
