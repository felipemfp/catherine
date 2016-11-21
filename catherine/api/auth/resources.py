import arrow
import jwt

from flask import Blueprint

from flask_restful import Api, Resource, marshal_with, reqparse, abort, fields
from flask_login import current_user, login_required

from catherine.api import app, db
from catherine.api.auth.models import User
from catherine.api.base import fields as custom_fields

auth_blueprint = Blueprint('api_auth', __name__)
api = Api(auth_blueprint, catch_all_404s=True)

user_fields = {
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'created_at': custom_fields.ArrowField(attribute='created_at')
}

token_fields = {
    'access_token': fields.String
}


class UserBase(Resource):

    def get_user(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404, message="User {} doesn't exist".format(username))
        return user


class UserDetail(UserBase):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('first_name', type=str)
    put_parser.add_argument('last_name', type=str)
    put_parser.add_argument('cur_password', type=str)
    put_parser.add_argument('new_password', type=str)

    @marshal_with(user_fields)
    @login_required
    def get(self, username):
        if username != current_user.username:
            abort(401)
        user = self.get_user(username)
        return user

    @login_required
    def delete(self, username):
        if username != current_user.username:
            abort(401)
        user = self.get_user(username)
        db.session.delete(user)
        db.session.commit()
        return {}, 204

    @marshal_with(user_fields)
    @login_required
    def put(self, username):
        if username != current_user.username:
            abort(401)
        args = self.put_parser.parse_args()
        user = self.get_user(username)
        # Update password if current one matches
        if None not in [args['cur_password'], args['new_password']]:
            if user.check_password(args['cur_password']):
                user.set_password(args['new_password'])
            else:
                abort(400, message='Invalid password')
        if args['first_name'] is not None:
            user.first_name = args['first_name']
        if args['last_name'] is not None:
            user.last_name = args['last_name']
        db.session.add(user)
        db.session.commit()
        return user, 200


class UserList(UserBase):

    parser = reqparse.RequestParser()
    parser.add_argument('first_name', type=str)
    parser.add_argument('last_name', type=str)
    parser.add_argument('username', type=str)
    parser.add_argument('password', type=str)

    @marshal_with(user_fields)
    def post(self):
        parsed_args = self.parser.parse_args()
        user = User(
            username=parsed_args['username'],
            first_name=parsed_args['first_name'],
            last_name=parsed_args['last_name']
        )
        user.set_password(parsed_args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201


class AuthToken(UserBase):

    token_parser = reqparse.RequestParser()
    token_parser.add_argument('username', type=str)
    token_parser.add_argument('password', type=str)

    @marshal_with(token_fields)
    def post(self):
        args = self.token_parser.parse_args()
        user = self.get_user(args['username'])
        if user.check_password(args['password']):
            iat = arrow.utcnow()
            token = jwt.encode({
                'username': user.username,
                'orig_iat': iat.timestamp,
                'iat': iat.timestamp,
                'exp': iat.replace(seconds=app.config.get('JWT_EXPIRATION_SECONDS')).timestamp
            }, app.config.get('SECRET_KEY'), algorithm=app.config.get('JWT_ALGORITHM'))
            return {'access_token': token.decode('utf-8')}, 200
        else:
            abort(401, message='Invalid login info')


class AuthRefreshToken(UserBase):
    token_parser = reqparse.RequestParser()
    token_parser.add_argument('token', type=str)

    @marshal_with(token_fields)
    def post(self):
        args = self.token_parser.parse_args()
        try:
            payload = jwt.decode(args['token'], app.config.get('SECRET_KEY'))
        except jwt.exceptions.ExpiredSignatureError:
            payload = jwt.decode(args['token'], verify=False)
        except:
            payload = None
        if payload is not None:
            iat = arrow.utcnow()
            orig_iat = arrow.get(payload['orig_iat'])
            exp_orig_iat = orig_iat.replace(
                seconds=app.config.get('JWT_REFRESH_EXPIRATION_SECONDS'))
            if exp_orig_iat.timestamp > iat.timestamp:
                token = jwt.encode({
                    'username': payload['username'],
                    'orig_iat': orig_iat.timestamp,
                    'iat': iat.timestamp,
                    'exp': iat.replace(seconds=app.config.get('JWT_EXPIRATION_SECONDS')).timestamp
                }, app.config.get('SECRET_KEY'), algorithm=app.config.get('JWT_ALGORITHM'))
                return {'access_token': token.decode('utf-8')}, 200
        abort(401, message='Invalid token')


api.add_resource(AuthToken, '/login/')
api.add_resource(AuthRefreshToken, '/login/refresh/')
api.add_resource(UserDetail, '/users/<string:username>')
api.add_resource(UserList, '/users/')
