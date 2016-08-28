# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =
'sqlite:////var/www/recipeshelf/database/recipeshelf.db'
db = SQLAlchemy(app)

class User(db.model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True)
    superuser = db.Column(db.Boolean)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


