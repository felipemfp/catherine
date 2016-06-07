from flask import request, json
from helpers import Crypt, Auth
from flask.views import MethodView
from models import db, User, Category, Person, Transaction, TransactionItem
from jose import jwt, JWTError
import config
import time


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message='Invalid Usage', status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def __str__(self):
        return '{}: {}'.format(self.status_code, self.message)


class BaseAPI(MethodView):
    def authenticate(self):
        token = request.headers.get('Authorization')
        if token:
            try:
                payload = jwt.decode(token.split(' ')[1], config.SECRET_KEY, algorithms=['HS256'])
                return User.query.get(payload['user_id'])
            except:
                raise InvalidUsage('Invalid Token', status_code=401)
        raise InvalidUsage('No token in header.', status_code=401)


class LoginAPI(BaseAPI):
    def post(self):
        supposed_user = request.get_json(force=True)
        user = User.query.filter_by(username=supposed_user['username']).first_or_404()
        if user and user.password == Crypt.hash_sha256(supposed_user['password']):
            token = jwt.encode({
                'exp': time.time() + 60 * 60 * 24 * 7,
                'user_id': user.user_id,
                'username': user.username,
                'name': user.name
                }, config.SECRET_KEY, algorithm='HS256')
            return json.jsonify({'token': token})
        raise InvalidUsage("Username and password does not match.")


class UserAPI(BaseAPI):
    def get(self, username):
        user = self.authenticate()
        if user:
            return json.jsonify(user.as_dict())
        raise InvalidUsage()

    def post(self):
        supposed_user = request.get_json(force=True)
        has_username_taken = User.query.filter_by(username=supposed_user['username']).first()
        if supposed_user and not has_username_taken:
            user = User()
            user.name = supposed_user['name']
            user.username = supposed_user['username']
            user.password = Crypt.hash_sha256(supposed_user['password'])
            db.session.add(user)
            db.session.commit()
            if user.user_id:
                return json.jsonify(user.as_dict())
        raise InvalidUsage()

    def put(self, username):
        user = self.authenticate()
        if user:
            new_user = request.get_json(force=True)
            user.name = new_user['name']
            user.username = new_user['username']
            user.password = Crypt.hash_sha256(new_user['password'])
            db.session.commit()
            return json.jsonify(user.as_dict())
        raise InvalidUsage()

    def delete(self, username):
        user = self.authenticate()
        if user:
            db.session.delete(user)
            db.session.commit()
            return json.jsonify({'success': '{} was deleted'.format(user)})
        raise InvalidUsage()


class CategoryAPI(BaseAPI):
    def get(self, username, category_id):
        user = self.authenticate()
        if user:
            if category_id:
                return json.jsonify(user.categories.filter_by(category_id=category_id).first_or_404().as_dict())
            return json.jsonify({'categories': [category.as_dict() for category in user.categories]})
        raise InvalidUsage()

    def post(self, username):
        user = self.authenticate()
        if user:
            supposed_category = request.get_json(force=True)
            category = Category()
            category.category_id = 1 if len(user.categories.all()) == 0 else user.categories.all()[-1].category_id + 1
            category.user_id = user.user_id
            category.name = supposed_category['name']
            category.icon = supposed_category['icon']
            db.session.add(category)
            db.session.commit()
            if category.category_id:
                return json.jsonify(category.as_dict())
        raise InvalidUsage()

    def put(self, username, category_id):
        user = self.authenticate()
        if user:
            new_category = request.get_json(force=True)
            category = user.categories.filter_by(category_id=category_id).first_or_404()
            category.name = new_category['name']
            category.icon = new_category['icon']
            db.session.commit()
            return json.jsonify(category.as_dict())
        raise InvalidUsage()

    def delete(self, username, category_id):
        user = self.authenticate()
        if user:
            category = user.categories.filter_by(category_id=category_id).first_or_404()
            if category:
                db.session.delete(category)
                db.session.commit()
                return json.jsonify({'success': '{} was deleted'.format(category)})
        raise InvalidUsage()


class PersonAPI(BaseAPI):
    def get(self, username, person_id):
        user = self.authenticate()
        if user:
            if person_id:
                return json.jsonify(user.people.filter_by(person_id=person_id).first_or_404().as_dict())
            return json.jsonify({'people': [person.as_dict() for person in user.people]})
        raise InvalidUsage()

    def post(self, username):
        user = self.authenticate()
        if user:
            supposed_person = request.get_json(force=True)
            person = Person()
            person.person_id = 1 if len(user.people.all()) == 0 else user.people.all()[-1].person_id + 1
            person.user_id = user.user_id
            person.name = supposed_person['name']
            db.session.add(person)
            db.session.commit()
            if person.person_id:
                return json.jsonify(person.as_dict())
        raise InvalidUsage()

    def put(self, username, person_id):
        user = self.authenticate()
        if user:
            new_person = request.get_json(force=True)
            person = user.people.filter_by(person_id=person_id).first_or_404()
            person.name = new_person['name']
            db.session.commit()
            return json.jsonify(person.as_dict())
        raise InvalidUsage()

    def delete(self, username, person_id):
        user = self.authenticate()
        if user:
            person = user.people.filter_by(person_id=person_id).first_or_404()
            if person:
                db.session.delete(person)
                db.session.commit()
                return json.jsonify({'success': '{} was deleted'.format(person)})
        raise InvalidUsage()


class TransactionAPI(BaseAPI):
    def get(self, username, transaction_id):
        user = self.authenticate()
        if user:
            if transaction_id:
                return json.jsonify(user.transactions.filter_by(transaction_id=transaction_id).first_or_404().as_dict())
            return json.jsonify({'transactions': [transaction.as_dict() for transaction in user.transactions]})
        raise InvalidUsage()

    def post(self, username):
        user = self.authenticate()
        if user:
            supposed_transaction = request.get_json(force=True)
            transaction = Transaction()
            transaction.transaction_id = 1 if len(user.transactions.all()) == 0 else user.transactions.all()[-1].transaction_id + 1
            transaction.user_id = user.user_id
            transaction.category_id = supposed_transaction['category_id']
            transaction.person_id = supposed_transaction['person_id']
            transaction.transaction_date = supposed_transaction['transaction_date']
            transaction.value = supposed_transaction['value']
            transaction.notes = supposed_transaction['notes']
            transaction.type = supposed_transaction['type']
            transaction.done = supposed_transaction['done']
            db.session.add(transaction)
            db.session.commit()
            if transaction.transaction_id:
                return json.jsonify(transaction.as_dict())
        raise InvalidUsage()

    def put(self, username, transaction_id):
        user = self.authenticate()
        if user:
            new_transaction = request.get_json(force=True)
            transaction = user.transactions.filter_by(transaction_id=transaction_id).first_or_404()
            transaction.category_id = new_transaction['category_id']
            transaction.person_id = new_transaction['person_id']
            transaction.transaction_date = new_transaction['transaction_date']
            transaction.value = new_transaction['value']
            transaction.notes = new_transaction['notes']
            transaction.type = new_transaction['type']
            transaction.done = new_transaction['done']
            db.session.commit()
            return json.jsonify(transaction.as_dict())
        raise InvalidUsage()

    def delete(self, username, transaction_id):
        user = self.authenticate()
        if user:
            transaction = user.transactions.filter_by(transaction_id=transaction_id).first_or_404()
            if transaction:
                db.session.delete(transaction)
                db.session.commit()
                return json.jsonify({'success': '{} was deleted'.format(transaction)})
        raise InvalidUsage()


class TransactionItemAPI(BaseAPI):
    def get(self, username, transaction_id, item_id):
        user = self.authenticate()
        if user:
            transaction = user.transactions.filter_by(transaction_id=transaction_id).first_or_404()
            if item_id:
                return json.jsonify(transaction.transaction_items.filter_by(item_id=item_id).first_or_404().as_dict())
            return json.jsonify({'transaction_items': [item.as_dict() for item in transaction.transaction_items]})
        raise InvalidUsage()

    def post(self, username, transaction_id):
        user = self.authenticate()
        if user:
            transaction = user.transactions.filter_by(transaction_id=transaction_id).first_or_404()
            supposed_item = request.get_json(force=True)
            item = TransactionItem()
            item.item_id = 1 if len(transaction.transaction_items.all()) else transaction.transaction_items.all()[-1].item_id + 1
            item.user_id = user.user_id
            item.transaction_id = transaction.transaction_id
            item.person_id = supposed_item['person_id']
            item.item_date = supposed_item['item_date']
            item.value = supposed_item['value']
            item.notes = supposed_item['notes']
            item.type = supposed_item['type']
            item.done = supposed_item['done']
            db.session.add(item)
            db.session.commit()
            if item.item_id:
                return json.jsonify(item.as_dict())
        raise InvalidUsage()

    def put(self, username, transaction_id, item_id):
        user = self.authenticate()
        if user:
            transaction = user.transactions.filter_by(transaction_id=transaction_id).first_or_404()
            new_item = request.get_json(force=True)
            item = transaction.transaction_items.filter_by(item_id=item_id).first_or_404()
            item.person_id = new_item['person_id']
            item.item_date = new_item['item_date']
            item.value = new_item['value']
            item.notes = new_item['notes']
            item.type = new_item['type']
            item.done = new_item['done']
            db.session.commit()
            return json.jsonify(item.as_dict())
        raise InvalidUsage()

    def delete(self, username, transaction_id, item_id):
        user = self.authenticate()
        if user:
            transaction = user.transactions.filter_by(transaction_id=transaction_id).first_or_404()
            item = transaction.transaction_items.filter_by(item_id=item_id).first_or_404()
            if item:
                db.session.delete(item)
                db.session.commit()
                return json.jsonify({'success': '{} was deleted'.format(item)})
        raise InvalidUsage()
