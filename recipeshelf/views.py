from flask import Flask, render_template, request, abort, url_for
from flask_sqlalchemy import SQLAlchemy
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
def hello():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/<int:error_code>")
def test_error(error_code):
    abort(error_code)

@app.route("/internal/db_actions")
def db_actions():
    db_action = request.args.get('action')
    controller.db_actions(db_action)
    return "Action complete."
