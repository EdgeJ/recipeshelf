"""
Views for the recipeshelf application

This module controls the routing, error handling, URL generation, and
sessions of the webpage.
"""
from os import urandom
from flask import abort, flash, Flask, redirect, render_template, request, session, url_for
import recipeshelf.controller

APP = Flask(__name__)
APP.secret_key = urandom(24)


# Error handling
# This dynamically routes all error codes from 400 to 599
for error_code in range(400, 599):
    @APP.errorhandler(error_code)
    def http_error_code(error):
        """
        Render error page for error code passed in as an argument.
        """
        return render_template('error.html', error=error.code), error.code


# Routing
@APP.route("/")
def index():
    """
    Render index page.
    """
    return render_template('index.html')


@APP.route("/login", methods=['GET', 'POST'])
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


@APP.route("/logout")
def logout():
    """
    Log the user out and return to the login page.
    """
    recipeshelf.controller.user_logout(user='username')
    flash('You are now logged out.')
    return redirect(url_for('login'))


@APP.route("/internal/db_actions")
def db_actions():
    """
    Perform database actions via HTTP GET method
    """
    return recipeshelf.controller.db_actions(
        action=request.args.get('action'),
        username=request.args.get('user'),
        email=request.args.get('email')
    )


@APP.route("/create_recipe", methods=['GET', 'POST'])
def create_recipe():
    if request.method == 'POST':
        title = request.form['title']
        cuisine_type = request.form['cuisine_type']
        primary_ingredient = request.form['primary_ingredient']
        user_id = ''
        serving_size = request.form['serving_size']
        body = ''
        quick_meal = False
        image_location = ''
        ingredients = request.form['ingredients'].split(',')
        #recipeshelf.controller.create_recipe(
        #    title, cuisine_type, primary_ingredient, user_id,
        #    serving_size, body, quick_meal, image_location, ingredients
        #)
        #return redirect('recipe', id=recipe_id)
        test_string = ''
        for i in (title, cuisine_type, primary_ingredient, user_id,
                  serving_size, body, quick_meal, image_location):
            test_string += ' {0}'.format(str(i))
        test_string += '<br>Ingredients:<br>'
        for i in ingredients:
            test_string += '{0}<br>'.format(str(i))
        return test_string
    return """
    <body>
      <form method="post">
        Title:<br>
        <input type="text" name="title"><br>
        Cuisine Type:<br>
        <input type="text" name="cuisine_type"><br>
        Main Ingredient:<br>
        <input type="text" name="primary_ingredient"><br>
        Serving Size:<br>
        <input type="text" name="serving_size"><br>
        Ingredients:<br>
        <input type="text" name="ingredients"><br>
        <input type="submit" value="Submit">
      </form>
    </body>
    """
    #    <textarea></textarea><br>
    #    <input type="submit" value="Submit">
    #  </form>
    #</body>
    #"""
