from flask import Blueprint

from flask_restful import Api, Resource, marshal_with, reqparse, abort, fields
from flask_login import current_user, login_required

from catherine.api import db
from catherine.api.categories.models import Category

categories_blueprint = Blueprint('api_categories', __name__)
api = Api(categories_blueprint, catch_all_404s=True)

category_fields = {
    'id': fields.Integer,
    'user': fields.String(attribute='user.username'),
    'description': fields.String
}


class CategoryBaseResource(Resource):

    def get_category(self, pk):
        category = Category.query.get_or_404(pk)
        if category.user_id != current_user.id:
            abort(400)
        return category


class CategoryDetail(CategoryBaseResource):

    put_parser = reqparse.RequestParser()
    put_parser.add_argument('description', type=str)

    @marshal_with(category_fields)
    @login_required
    def get(self, pk):
        return self.get_category(pk)

    @marshal_with(category_fields)
    @login_required
    def put(self, pk):
        args = self.put_parser.parse_args()
        category = self.get_category(pk)
        if args['description'] is not None:
            category.description = args['description']
        db.session.add(category)
        db.session.commit()
        return category, 200

    @login_required
    def delete(self, pk):
        category = self.get_category(pk)
        db.session.delete(category)
        db.session.commit()
        return {}, 204


class CategoryList(CategoryBaseResource):

    parser = reqparse.RequestParser()
    parser.add_argument('description', type=str, required=True)

    @marshal_with(category_fields)
    @login_required
    def get(self):
        return current_user.categories.all()

    @login_required
    def post(self):
        args = self.parser.parse_args()
        category = Category(
            description=args['description'],
            user=current_user
        )
        db.session.add(category)
        db.session.commit()
        return {}, 201

api.add_resource(CategoryList, '/categories/')
api.add_resource(CategoryDetail, '/categories/<int:pk>/')
