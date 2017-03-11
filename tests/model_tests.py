"""
Testing module for recipeshelf models.  Using SQLAlchemy and Flask Testing
modules.
"""
import sys
from flask-testing import TestCase

sys.path.insert(0, '../recipeshelf')
from models import create_app, DB


class UserCreate(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
    TESTING = True

    def create_app(self):
        # no idea what's supposed to go here
        return create_app(self)

    def setup(self):
        DB.create_all()

    def teardown(self):
        DB.session.remove()
        DB.drop_all()

    def test_create(self):
        user = User()
        DB.session.add(user)
        DB.session.commit()
        assert user in DB.session
        response = self.client.get("/")
