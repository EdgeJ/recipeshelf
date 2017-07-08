from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from recipeshelf import app

db = SQLAlchemy(app)
recipe_ingredients = db.Table(
    'recipe_ingredients',
    db.Column(
        'recipe_id',
        db.Integer,
        db.ForeignKey('recipe.id')
    ),
    db.Column(
        'ingredient_id',
        db.Integer,
        db.ForeignKey('ingredient.id')
    )
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(20), unique=True)
    superuser = db.Column(db.Boolean)
    recipes_created = db.relationship(
        'Recipe', backref=db.backref('user'), lazy='dynamic'
    )

    def __init__(self, username, password, email, superuser=False):
        self.username = username
        self.password = password
        self.email = email
        self.superuser = superuser

    def __repr__(self):
        return '<User %r>' % self.username


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)
    date_added = db.Column(db.DateTime)
    image_location = db.Column(db.String(80))
    quick_meal = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ingredients = db.relationship(
        'Ingredient', secondary=recipe_ingredients,
        backref=db.backref('recipe_using'), lazy='dynamic'
    )
    recipe_contents = db.relationship(
        'RecipeContents', backref=db.backref('recipe_using'), uselist=False
    )

    def __init__(self, title):
        self.title = title
        self.date_added = datetime.utcnow()
        self.quick_meal = False

    def __repr__(self):
        return '<Title %r>' % self.title


class RecipeContents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    meal_type = db.Column(db.String(40))
    primary_ingredient = db.Column(db.String(40))
    serving_size = db.Column(db.Integer)
    body = db.Column(db.Text)

    def __init__(self, meal_type, primary_ingredient,
                 serving_size, body=None):
        self.meal_type = meal_type
        self.primary_ingredient = primary_ingredient
        self.serving_size = serving_size
        self.body = body

    def __repr__(self):
        return '<Body %r>' % self.body


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40))
    amount = db.Column(db.String(20))

    def __init__(self, name, amount):
        self.name = name.lower()
        self.amount = amount.lower()

    def __repr__(self):
        return '<Name %r>' % self.name
