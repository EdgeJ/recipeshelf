from flask import Flask, render_template, request, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from models import *

def db_actions(action, username):
    case = {
            'create': db.create_all(),
            'destroy': db.drop_all(),
            'newuser': create_user(username, email='example@site.com'),
            }
    return case.get(action, None)

def create_user(username, email, superuser=False):
    password = None
    new_user = User(username, password, email, superuser)
    db.session.add(new_user)
    db.session.commit

def create_recipe(
        id, title, cuisine_type, primary_ingredient, user_id,
        serving_size, body, quick_meal, image_location, *ingredients
        ):
    next_id = Recipe.query.filterby(id).last() + 1
    new_recipe = Recipe(next_id, title, image_location, cuisine_type,
                        user_id, quick_meal)
    new_recipe_body = RecipeContents(next_id, primary_ingredient,
                                    serving_size, body)
    for ingredient in ingredients:
        if not Ingredient.query.filter_by(ingredient):
            new_ingredient = Ingredient(ingredient)
            db.session.add(new_ingredient)
    db.session.commit()

def user_login(username, password):
    if User.query.filter_by(username):
        pass
        return True
    return False
