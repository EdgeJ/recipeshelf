from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import recipeshelf.settings

APP = Flask(__name__)
APP.config[
    'SQLALCHEMY_DATABASE_URI'
] = recipeshelf.settings.SQLALCHEMY_DATABASE_URI
DB = SQLAlchemy(APP)
RECIPE_INGREDIENTS = DB.Table(
    'recipe_ingredients',
    DB.Column(
        'recipe_id',
        DB.Integer,
        DB.ForeignKey('recipe.id')
    ),
    DB.Column(
        'ingredient_id',
        DB.Integer,
        DB.ForeignKey('ingredient.id')
    )
)


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(10), unique=True)
    password = DB.Column(DB.String(20))
    email = DB.Column(DB.String(20), unique=True)
    superuser = DB.Column(DB.Boolean)
    recipes_created = DB.relationship(
        'Recipe', backref=DB.backref('user'), lazy='dynamic'
    )

    def __init__(self, username, password, email, superuser=False):
        self.username = username
        self.password = password
        self.email = email
        self.superuser = superuser

    def __repr__(self):
        return '<User %r>' % self.username


class Recipe(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.Text, unique=True)
    date_added = DB.Column(DB.DateTime)
    image_location = DB.Column(DB.String(80))
    quick_meal = DB.Column(DB.Boolean)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'))
    ingredients = DB.relationship(
        'Ingredient', secondary=RECIPE_INGREDIENTS,
        backref=DB.backref('recipe_using'), lazy='dynamic'
    )
    recipe_contents = DB.relationship(
        'RecipeContents', backref=DB.backref('recipe_using'), uselist=False
    )

    def __init__(self, title):
        self.title = title
        self.date_added = datetime.utcnow()
        self.quick_meal = False

    def __repr__(self):
        return '<Title %r>' % self.title


class RecipeContents(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    recipe_id = DB.Column(DB.Integer, DB.ForeignKey('recipe.id'))
    meal_type = DB.Column(DB.String(40))
    primary_ingredient = DB.Column(DB.String(40))
    serving_size = DB.Column(DB.Integer)
    body = DB.Column(DB.Text)

    def __init__(self, meal_type, primary_ingredient,
                 serving_size, body=None):
        self.meal_type = meal_type
        self.primary_ingredient = primary_ingredient
        self.serving_size = serving_size
        self.body = body

    def __repr__(self):
        return '<Body %r>' % self.body


class Ingredient(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True, unique=True)
    name = DB.Column(DB.String(40))
    amount = DB.Column(DB.String(20))

    def __init__(self, name, amount):
        self.name = name.lower()
        self.amount = amount.lower()

    def __repr__(self):
        return '<Name %r>' % self.name
