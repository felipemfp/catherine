# catherine/api/__init__.py

from collections import OrderedDict

from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt import JWT
from decouple import config


# config

app = Flask(__name__)

app_settings = config('APP_SETTINGS', 'integrada.api.config.ProductionConfig')
app.config.from_object(app_settings)


# extensions

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})
