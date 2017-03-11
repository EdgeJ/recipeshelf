from flask import Flask, render_template, request, abort, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import *


def db_actions(action=None, username=None, email=''):
    if action == 'create':
        DB.create_all()
        return 'Database created.'
    if action == 'destroy':
        DB.drop_all()
        return 'Databased cleared.'
    if action == 'newuser':
        create_user(username, email)
        return 'User {0} created.'.format(username)
    if action is None:
        return False


def create_user(username, email, superuser=False):
    password = None
    new_user = User(username, password, email, superuser)
    DB.session.add(new_user)
    DB.session.commit()


def create_recipe(
        title, cuisine_type, primary_ingredient, user_id,
        serving_size, body, quick_meal, image_location=None, *ingredients
):
    next_id = Recipe.query.filterby(id).last() + 1
    new_recipe = Recipe(next_id, title, image_location, cuisine_type,
                        user_id, quick_meal)
    new_recipe_body = RecipeContents(next_id, primary_ingredient,
                                     serving_size, body)
    for ingredient in ingredients:
        if not Ingredient.query.filter_by(ingredient):
            new_ingredient = Ingredient(ingredient)
            DB.session.add(new_ingredient)
    DB.session.commit()


def user_login(user_login, password):
    if User.query.filter_by(username=str(user_login)):
        user = User.query.filter_by(username=str(user_login)).first()
    if user is not None:
        session['username'] = user_login
        return user.id
    return False


def user_logout():
    return session.pop['username', None]
