from flask import Flask, render_template, request, abort, url_for
import controller
app = Flask(__name__)

# Error handling
#-----------------------------------------------------------------------------#

def http_error(error):
    return render_template('error.html', error=error.code)

#a little clunky, but it dynamically routes all errors
for error in (range(400, 599)):
    app.error_handler_spec[None][error] = http_error

# Routing
#-----------------------------------------------------------------------------#
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if controller.user_login(
                request.form['username'], request.form['password']
                ):
            return redirect(url_for('index'))
        else:
            error = 'Invalid login.'
    return render_template('login.html', error=None)

@app.route("/<int:error_code>")
def test_error(error_code):
    abort(error_code)

@app.route("/internal/db_actions")
def db_actions():
    db_action = request.args.get('action')
    username = request.args.get('user')
    controller.db_actions(db_action, username=None)
    return "Action complete."
