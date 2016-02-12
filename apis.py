from flask import request, json
from helpers import Crypt, Auth
from flask.views import MethodView
from models import db, User, Category, Person, Transaction, TransactionItem


class UserAPI(MethodView):
    def get(self, user_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            return json.jsonify(user.as_dict())
        return json.jsonify({})

    def post(self):
        supposed_user = request.get_json(force=True)
        if supposed_user:
            user = User()
            user.name = supposed_user['name']
            user.login = supposed_user['login']
            user.password = Crypt.hash_sha256(supposed_user['password'])
            user.auth_key = Auth.get_new_key()
            db.session.add(user)
            db.session.commit()
            if user.user_id:
                return json.jsonify(user.as_dict())
        return json.jsonify({})

    def put(self, user_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            new_user = request.get_json(force=True)
            user.name = new_user['name']
            user.login = new_user['login']
            user.password = Crypt.hash_sha256(new_user['password'])
            db.session.commit()
            return json.jsonify(user.as_dict())
        return json.jsonify({})

    def delete(self, user_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            db.session.delete(user)
            db.session.commit()
            return json.jsonify({'success': '{} was deleted'.format(user)})
        return json.jsonify({})


class LoginAPI(MethodView):
    def post(self):
        supposed_user = request.get_json(force=True)
        user = User.query.filter_by(login=supposed_user['login']).first_or_404()
        if user and user.password == Crypt.hash_sha256(supposed_user['password']):
            return json.jsonify(user.as_dict())
        return json.jsonify({})


class CategoryAPI(MethodView):
    def get(self, user_id, category_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            if category_id:
                return json.jsonify(user.categories.filter_by(category_id=category_id).first_or_404().as_dict())
            return json.jsonify({'categories': [category.as_dict() for category in user.categories]})
        return json.jsonify({})

    def post(self, user_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            supposed_category = request.get_json(force=True)
            category = Category()
            category.user_id = user_id
            category.name = supposed_category['name']
            category.icon_id = supposed_category['icon_id']
            db.session.add(category)
            db.session.commit()
            if category.category_id:
                return json.jsonify(category.as_dict())
        return json.jsonify({})

    def put(self, user_id, category_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            new_category = request.get_json(force=True)
            category = user.categories.filter_by(category_id=category_id).first_or_404()
            category.name = new_category['name']
            category.icon_id = new_category['icon_id']
            db.session.commit()
            return json.jsonify(category.as_dict())
        return json.jsonify({})

    def delete(self, user_id, category_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            category = user.categories.filter_by(category_id=category_id).first_or_404()
            if category:
                db.session.delete(category)
                db.session.commit()
                return json.jsonify({'success': '{} was deleted'.format(category)})
        return json.jsonify({})


class PersonAPI(MethodView):
    def get(self, user_id, person_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            if person_id:
                return json.jsonify(user.people.filter_by(person_id=person_id).first_or_404().as_dict())
            return json.jsonify({'people': [person.as_dict() for person in user.people]})
        return json.jsonify({})

    def post(self, user_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            supposed_person = request.get_json(force=True)
            person = Person()
            person.user_id = user_id
            person.name = supposed_person['name']
            db.session.add(person)
            db.session.commit()
            if person.person_id:
                return json.jsonify(person.as_dict())
        return json.jsonify({})

    def put(self, user_id, person_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            new_person = request.get_json(force=True)
            person = user.people.filter_by(person_id=person_id).first_or_404()
            person.name = new_person['name']
            db.session.commit()
            return json.jsonify(person.as_dict())
        return json.jsonify({})

    def delete(self, user_id, person_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            person = user.people.filter_by(person_id=person_id).first_or_404()
            if person:
                db.session.delete(person)
                db.session.commit()
                return json.jsonify({'success': '{} was deleted'.format(person)})
        return json.jsonify({})


class TransactionAPI(MethodView):
    def get(self, user_id, transaction_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            if transaction_id:
                return json.jsonify(user.transactions.filter_by(transaction_id=transaction_id).first_or_404().as_dict())
            return json.jsonify({'transactions': [transaction.as_dict() for transaction in user.transactions]})
        return json.jsonify({})

    def post(self, user_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            supposed_transaction = request.get_json(force=True)
            transaction = Transaction()
            transaction.user_id = user_id
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
        return json.jsonify({})

    def put(self, user_id, transaction_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
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
        return json.jsonify({})

    def delete(self, user_id, transaction_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            transaction = user.transactions.filter_by(transaction_id=transaction_id).first_or_404()
            if transaction:
                db.session.delete(transaction)
                db.session.commit()
                return json.jsonify({'success': '{} was deleted'.format(transaction)})
        return json.jsonify({})


class TransactionItemAPI(MethodView):
    def get(self, user_id, transaction_id, item_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            transaction = user.transactions.filter_by(transaction_id=transaction_id).first_or_404()
            if item_id:
                return json.jsonify(transaction.transaction_items.filter_by(item_id=item_id).first_or_404().as_dict())
            return json.jsonify({'transaction_items': [item.as_dict() for item in transaction.transaction_items]})
        return json.jsonify({})

    def post(self, user_id, transaction_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            transaction = user.transactions.filter_by(transaction_id=transaction_id).first_or_404()
            supposed_item = request.get_json(force=True)
            item = TransactionItem()
            item.user_id = user_id
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
        return json.jsonify({})

    def put(self, user_id, transaction_id, item_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
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
        return json.jsonify({})

    def delete(self, user_id, transaction_id, item_id):
        auth_key = request.args.get('key')
        user = User.authenticate(user_id, auth_key)
        if user:
            transaction = user.transactions.filter_by(transaction_id=transaction_id).first_or_404()
            item = transaction.transaction_items.filter_by(item_id=item_id).first_or_404()
            if item:
                db.session.delete(item)
                db.session.commit()
                return json.jsonify({'success': '{} was deleted'.format(item)})
        return json.jsonify({})