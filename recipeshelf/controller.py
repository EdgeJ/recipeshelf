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
        try:
            create_user(username, email)
        except:
            DB.session.rollback()
            return 'User {} could not be created'.format(username)
        return 'User {} created.'.format(username)
    if action is None:
        return False


def create_user(username, email, superuser=False):
    password = None
    new_user = User(username, password, email, superuser)
    DB.session.add(new_user)
    DB.session.commit()


def update_password(password):
    pass


def get_all_recipes():
    return Recipe.query.all()


def create_recipe(
        title, meal_type, primary_ingredient, user,
        serving_size, body, quick_meal, ingredients, image_location=None
):
    new_recipe = Recipe(title)
    if image_location is not None:
        new_recipe.image_location = image_location
    if quick_meal:
        new_recipe.quick_meal = True
    new_recipe_contents = RecipeContents(
        meal_type, primary_ingredient, serving_size, body
    )
    new_recipe.recipe_contents = new_recipe_contents
    for ingredient in ingredients:
        new_ingredient = Ingredient(ingredient)
        new_recipe.ingredients.append(new_ingredient)
        DB.session.add(new_ingredient)
    DB.session.add(new_recipe)
    DB.session.add(new_recipe_contents)
    DB.session.commit()
    return new_recipe.id


def view_recipe(recipe_id):
    return Recipe.query.get_or_404(recipe_id)


def view_ingredient(ingredient_name):
    return Ingredient.query.filter_by(name=ingredient_name).first()


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
