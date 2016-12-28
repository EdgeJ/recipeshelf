"""
Testing module for recipeshelf models.  Using SQLAlchemy and Flask Testing
modules.
"""
import sys
from flask-testing import TestCase

sys.path.insert(0, '../recipeshelf')
from models import create_app, db

class UserCreate(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
    TESTING = True

    def create_app(self):
        # no idea what's supposed to go here
        return create_app(self)

    def setup(self):
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_create(self):
        user = User()
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        response = self.client.get("/")
