"""
Testing module for recipeshelf models.  Using SQLAlchemy and Flask Testing
modules.
"""
import sys
import unittest
from flask import Flask
from flask_testing import TestCase
sys.path.insert(0, '../recipeshelf')
from recipeshelf.models import DB, User


class TestUserCreate(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
    TESTING = True

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

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

if __name__ == '__main__':
    unittest.main()
