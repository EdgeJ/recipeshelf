from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import recipeshelf.settings

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = recipeshelf.settings.SQLALCHEMY_DATABASE_URI
DB = SQLAlchemy(APP)


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(10), unique=True)
    password = DB.Column(DB.String(20))
    email = DB.Column(DB.String(20), unique=True)
    superuser = DB.Column(DB.Boolean)
    recipes = DB.relationship('Recipe', backref='user', lazy='dynamic')

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
    image_location = DB.Column(DB.String(80))
    cuisine_type = DB.Column(DB.String(40))
    ingredient = DB.relationship('Ingredients', backref='recipe',
                                 lazy='dynamic')
    quick_meal = DB.Column(DB.Boolean)
    date_added = DB.Column(DB.DateTime)
    user_id = DB.Column(DB.String(10), DB.ForeignKey('user.id'))
    recipe_contents = DB.relationship('RecipeContents', backref='recipe',
                                      lazy='dynamic')

    def __init__(self, id, title, image_location, cuisine_type, ingredient,
                 user_id, quick_meal):
        self.title = title
        self.image_location = image_location
        self.meal_type = meal_type
        self.quick_meal = quick_meal
        self.date_added = datetime.utcnow()
        self.recipe_contents = recipe_contents

    def __repr__(self):
        return '<Title %r>' % self.title


class RecipeContents(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    recipe_id = DB.Column(DB.Integer, DB.ForeignKey('recipe.id'))
    primary_ingredient = DB.Column(DB.String(40))
    serving_size = DB.Column(DB.Integer)
    body = DB.Column(DB.Text)

    def __init__(self, recipe_id, primary_ingredient, serving_size, body=None):
        self.recipe_id = recipe_id
        self.primary_ingredient = primary_ingredient
        self.serving_size = serving_size
        self.cuisine_type = cuisine_type
        self.body = body

    def __repr__(self):
        return '<Body %r>' % self.body


class Ingredients(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True, unique=True)
    name = DB.Column(DB.String(40))
    recipe_using = DB.Column(DB.String(10), DB.ForeignKey('recipe.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Name %r>' % self.name
