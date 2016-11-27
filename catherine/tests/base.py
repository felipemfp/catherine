from flask_testing import TestCase

from catherine.api import app, db


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('catherine.api.config.TestingConfig')
        return app

    def login(self, username, password):
        return self.client.post('/login/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def register(self, username, password, first_name=None, last_name=None):
        return self.client.post('/register/', data=dict(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        ), follow_redirects=True)

    def login_and_register(self, username, password, first_name=None, last_name=None):
        self.register(username, password, first_name, last_name)
        return self.login(username, password)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
