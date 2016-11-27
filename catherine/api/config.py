# project/server/config.py

import os
from decouple import config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = config('SECRET_KEY')
    DEBUG = config('DEBUG', default=False, cast=bool)
    BCRYPT_LOG_ROUNDS = config('BCRYPT_LOG_ROUNDS', default=13, cast=int)
    SQLALCHEMY_TRACK_MODIFICATIONS = config(
        'SQLALCHEMY_TRACK_MODIFICATIONS', default=False, cast=bool)
    JWT_ALGORITHM = config('JWT_ALGORITHM', default='HS256')
    JWT_EXPIRATION_SECONDS = config(
        'JWT_EXPIRATION_SECONDS', default=300, cast=int)
    JWT_REFRESH_EXPIRATION_SECONDS = config(
        'JWT_REFRESH_EXPIRATION_SECONDS', default=7 * 24 * 60 * 60, cast=int)
    JWT_AUTH_HEADER_PREFIX = config('JWT_AUTH_HEADER_PREFIX', default='JWT')
    BUNDLE_ERRORS = config('BUNDLE_ERRORS', default=True, cast=bool)


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(BASE_DIR, 'dev.sqlite')


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/catherine'
