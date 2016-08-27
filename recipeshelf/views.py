from flask import Flask, render_template, request, abort, url_for
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
    return "Hello World!"

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/502")
def test_502():
    abort(502)

@app.route("/403")
def test_403():
    abort(403)
