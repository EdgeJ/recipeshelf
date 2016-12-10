from flask import Flask, render_template, request, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from models import *

def db_actions(action):
    case = {
            'create': db.create_all(),
            'destroy': db.drop_all(),
            }
    return case.get(action, None)
