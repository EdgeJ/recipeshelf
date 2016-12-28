from flask import Flask, render_template, request, abort, url_for, redirect, session
import controller
from os import urandom

app = Flask(__name__)
app.secret_key = urandom(24)

# Error handling
#-----------------------------------------------------------------------------#

def http_error(error):
    return render_template('error.html', error=error.code), error.code

#a little clunky, but it dynamically routes all errors
for error in (range(400, 599)):
    app.error_handler_spec[None][error] = http_error

@app.route("/<int:error_code>")
def test_error(error_code):
    abort(error_code)

# Routing
#-----------------------------------------------------------------------------#
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if controller.user_login(
                request.form['username'], request.form['password']
                ):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            error = 'Invalid login.'
    return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/internal/db_actions")
def db_actions():
    return controller.db_actions(
            action=request.args.get('action'), username=request.args.get('user')
            )

@app.route("/create_recipe", methods=['GET', 'POST'])
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
        #controller.create_recipe(
        #    title, cuisine_type, primary_ingredient, user_id,
        #    serving_size, body, quick_meal, image_location, ingredients
        #)
        #return redirect('recipe', id=recipe_id)
        test_string = ''
        for i in title, cuisine_type, primary_ingredient, user_id, serving_size, body, quick_meal, image_location:
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
