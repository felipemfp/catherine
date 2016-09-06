import os

ENV = os.environ.get('ENV', 'Development')
DEBUG = False if ENV == 'Production' else True
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL', 'sqlite:////tmp/dev.db')
SECRET_KEY = os.environ.get('SECRET_KEY', default='Not my real secret')
