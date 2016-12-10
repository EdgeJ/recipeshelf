from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'
    ] = 'sqlite:////usr/local/www/database/recipeshelf.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True)
    superuser = db.Column(db.Boolean)
    recipes = db.relationship('Recipe', backref='user', lazy='dynamic')

    def __init__(self, username, password, email, superuser=False):
        self.username = username
        self.password = password
        self.email = email
        self.superuser = superuser

    def __repr__(self):
        return '<User %r>' % self.username

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)
    image_location = db.Column(db.String(80))
    cuisine_type = db.Column(db.String(40))
    ingredient = db.relationship('Ingredients', backref='recipe',
                                 lazy='dynamic')
    quick_meal = db.Column(db.Boolean)
    date_added = db.Column(db.DateTime)
    user_id = db.Column(db.String(10), db.ForeignKey('user.id'))
    recipe_contents = db.relationship('RecipeContents', backref='recipe',
                                      lazy='dynamic')

    def __init__(self, title, image_location, cuisine_type, ingredient,
                 user_id, quick_meal):
       self.title = title
       self.image_location = image_location
       self.meal_type = meal_type
       self.quick_meal = quick_meal
       self.recipe_contents = recipe_contents

    def __repr__(self):
        return '<Title %r>' % self.title

class RecipeContents(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    primary_ingredient = db.Column(db.String(40))
    serving_size = db.Column(db.Integer)
    body = db.Column(db.Text)

    def __init__(self, recipe_id, primary_ingredient, serving_size, body=None):
        self.recipe_id = recipe_id
        self.primary_ingredient = primary_ingredient
        self.serving_size = serving_size
        self.cuisine_type = cuisine_type
        self.body = body

    def __repr__(self):
        return '<Body %r>' % self.body

class Ingredients(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    name = db.Column(db.String(40))
    recipe_using = db.Column(db.String(10), db.ForeignKey('recipe.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Name %r>' % self.name
