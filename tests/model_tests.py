"""
Testing module for recipeshelf models.  Using SQLAlchemy and Flask Testing
modules.
"""
import sys
import unittest
from flask import Flask
from flask_testing import TestCase
sys.path.insert(0, '../recipeshelf')
from recipeshelf.models import db, User


class TestUserCreate(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
    TESTING = True

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./test.db"
        return app

    def setup(self):
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_create(self):
        user = User('John Smith', 'changeme', 'mail@example.com')
        db.session.add(user)
        db.session.commit()
        assert user in db.session
        response = self.client.get("/")


if __name__ == '__main__':
    unittest.main()
