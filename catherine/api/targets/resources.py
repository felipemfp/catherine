from flask import Blueprint

from flask_restful import Api, Resource, marshal_with, reqparse, abort, fields
from flask_login import current_user, login_required

from catherine.api import db
from catherine.api.targets.models import Target, TargetType

targets_blueprint = Blueprint('api_targets', __name__)
api = Api(targets_blueprint, catch_all_404s=True)


target_type_fields = {
    'id': fields.Integer,
    'description': fields.String
}

target_fields = {
    'id': fields.Integer,
    'user': fields.String(attribute='user.username'),
    'description': fields.String,
    'target_type': fields.Nested(target_type_fields)
}


class TargetBaseResource(Resource):

    def get_target_type(self, pk):
        return TargetType.query.get(pk)

    def get_target(self, pk):
        target = Target.query.get_or_404(pk)
        if target.user_id != current_user.id:
            abort(400)
        return target


class TargetTypeList(TargetBaseResource):

    @marshal_with(target_type_fields)
    @login_required
    def get(self):
        return TargetType.query.all()


class TargetDetail(TargetBaseResource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('description', type=str)
    put_parser.add_argument('target_type', type=int)

    @marshal_with(target_fields)
    @login_required
    def get(self, pk):
        return self.get_target(pk)

    @login_required
    def put(self, pk):
        args = self.put_parser.parse_args()
        target = self.get_target(pk)
        if args['description'] is not None:
            target.description = args['description']
        if args['target_type'] is not None:
            if self.get_target_type(args['target_type']) is not None:
                target.target_type_id = args['target_type']
        db.session.add(target)
        db.session.commit()
        return target, 200

    @login_required
    def delete(self, pk):
        target = self.get_target(pk)
        db.session.delete(target)
        db.session.commit()
        return {}, 204


class TargetList(TargetBaseResource):

    parser = reqparse.RequestParser()
    parser.add_argument('description', type=str, required=True)
    parser.add_argument('target_type', type=int, required=True)

    @marshal_with(target_fields)
    @login_required
    def get(self):
        return current_user.targets.all()

    @login_required
    def post(self):
        args = self.parser.parse_args()
        target_type = self.get_target_type(args['target_type'])
        if target_type is None:
            abort(400)
        target = Target(
            description=args['description'],
            user=current_user,
            target_type=target_type
        )
        db.session.add(target)
        db.session.commit()
        return {}, 201


api.add_resource(TargetTypeList, '/target_types/')
api.add_resource(TargetList, '/targets/')
api.add_resource(TargetDetail, '/targets/<int:pk>/')
