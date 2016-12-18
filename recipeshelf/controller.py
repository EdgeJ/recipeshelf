from flask import Flask, render_template, request, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from models import *

def db_actions(action=None, username=None):
    if action == 'create':
        db.create_all()
        return 'Database created.'
    if action == 'destroy':
        db.drop_all()
        return 'Databased cleared.'
    if action == 'newuser':
        create_user(username, email='example@site2.com')
        return 'User {0} created.'.format(username)
    if action == None:
        return False

def create_user(username, email, superuser=False):
    password = None
    new_user = User(username, password, email, superuser)
    db.session.add(new_user)
    db.session.commit()

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

def user_login(user_login, password):
    if User.query.filter_by(username=str(user_login)):
        user = User.query.filter_by(username=str(user_login)).first()
    if user != None:
        return user.id
    return False
