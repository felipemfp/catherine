import os

ENV = os.environ.get('ENV', 'Development')
DEBUG = False if ENV == 'Production' else True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:////tmp/dev.db')
