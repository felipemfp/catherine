# catherine/api/__init__.py


from collections import OrderedDict

from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from flask_restful import abort

import jwt
from decouple import config


# config

app = Flask(__name__)

app_settings = config('APP_SETTINGS', 'integrada.api.config.ProductionConfig')
app.config.from_object(app_settings)


# extensions

login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# flask_login

from catherine.api.auth.models import User


@login_manager.request_loader
def load_user_from_request(request):
    header = request.headers.get('Authorization')
    if not header:
        return None
    prefix, token = header.split()
    if prefix.lower() != app.config.get('JWT_AUTH_HEADER_PREFIX').lower():
        return None
    try:
        payload = jwt.decode(token, app.config.get('SECRET_KEY'))
        return User.query.filter_by(username=payload['username']).first()
    except:
        return None


@login_manager.unauthorized_handler
def unauthorized():
    return abort(401)


# blueprints

from catherine.api.auth.resources import auth_blueprint
from catherine.api.categories.resources import categories_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(categories_blueprint)
