from flask import Flask, render_template, request, abort, url_for, session
from flask_sqlalchemy import SQLAlchemy
from recipeshelf.models import *


def db_actions(action=None, username=None, email=''):
    if action == 'create':
        DB.create_all()
        return 'Database created.'
    if action == 'destroy':
        DB.session.rollback()
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


def update_password(password):
    pass


def create_recipe(
        title, meal_type, primary_ingredient, user_id,
        serving_size, body, quick_meal, ingredients, image_location=None
):
    new_recipe = Recipe(title, meal_type, quick_meal)
    DB.session.add(new_recipe)
    new_recipe_body = RecipeContents(new_recipe.id, primary_ingredient,
                                     serving_size, body)
    DB.session.add(new_recipe_body)
    all_ingredients = Ingredients.query.all()
    for ingredient in ingredients:
        if ingredient not in all_ingredients:
            new_ingredient = Ingredients(new_recipe.id, ingredient)
            DB.session.add(new_ingredient)
    DB.session.commit()


def user_login(user_login, password):
    if User.query.filter_by(username=str(user_login)):
        user = User.query.filter_by(username=str(user_login)).first()
    if user is not None:
        session['username'] = user_login
        return user.id
    return False


def user_logout(user=None):
    """
    Pop the current user out of the session.
    """
    return session.pop(user, None)
