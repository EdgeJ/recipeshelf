"""
Views for the recipeshelf application

This module controls the routing, error handling, URL generation, and
sessions of the webpage.
"""
from flask import abort, flash, redirect, render_template, request, session, url_for
from recipeshelf import app
import recipeshelf.controller

# Error handling
# This dynamically routes all error codes from 400 to 599
for error_code in range(400, 599):
    @app.errorhandler(error_code)
    def http_error_code(error):
        """
        Render error page for error code passed in as an argument.
        """
        return render_template('error.html', error=error.code), error.code


# Routing
@app.route("/")
def index():
    """
    Render index page.
    """
    return render_template('index.html')


@app.route("/internal/db_actions", methods=['POST', 'DELETE'])
def db_actions():
    """
    Perform database actions via HTTP GET method
    """
    return recipeshelf.controller.db_actions(
        action=request.args.get('action'),
        username=request.args.get('user'),
        email=request.args.get('email')
    )


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        flash('You are already logged in.')
        return render_template('index.html')
    if request.method == 'POST':
        if recipeshelf.controller.user_login(
                request.form['username'], request.form['password']
        ):
            session['username'] = request.form['username']
            flash('You are now logged in.')
            return redirect(url_for('index'))
        else:
            return render_template(
                'login.html', error='Invalid login.'
            )
    else:
        return render_template('login.html')


@app.route("/logout")
def logout():
    """
    Log the user out and return to the login page.
    """
    recipeshelf.controller.user_logout(user='username')
    flash('You are now logged out.')
    return redirect(url_for('login'))


@app.route("/create_recipe", methods=['GET', 'POST'])
def create_recipe():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['title']
            meal_type = request.form['meal_type']
            primary_ingredient = request.form['primary_ingredient']
            body = request.form['body']
            quick_meal = bool(request.form['quick_meal'])
            serving_size = request.form['serving_size']
            user_id = session['username']
            image_location = ''
            ingredients = request.form['ingredients'].split(',')
            new_recipe_id = recipeshelf.controller.create_recipe(
                title, meal_type, primary_ingredient, user_id,
                serving_size, body, quick_meal, ingredients, image_location
            )
            return redirect(url_for('view_recipe', recipe_id=new_recipe_id))
        else:
            return render_template('create_recipe.html')
    else:
        flash('Please log in to post a recipe.')
        return redirect(url_for('login'))


@app.route("/recipes")
def show_all_recipes():
    return render_template(
        'all_recipes.html', recipes=recipeshelf.controller.get_all_recipes()
    )


@app.route("/recipe/test")
def test_create_recipe():
    new_recipe_id = recipeshelf.controller.create_recipe(
        'test', 'test type', 'primary_ingredient', 'test user_id',
        '1', 'Lorum ipsum dolor si amet', False, ['ingredients'], None
    )
    return redirect(url_for('view_recipe', recipe_id=new_recipe_id))


@app.route("/recipe/<int:recipe_id>")
def view_recipe(recipe_id):
    recipe = recipeshelf.controller.view_recipe(recipe_id)
    return render_template('recipe.html', recipe=recipe)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        recipeshelf.controller.db_actions(
            action='newuser', username=username, email=email
        )
        recipeshelf.controller.update_password(password)
        flash('User {} created'.format(username))
        return redirect(url_for('login'))
    else:
        return render_template('create_user.html')
