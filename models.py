from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    login = db.Column(db.String(50))
    password = db.Column(db.String(64))
    auth_key = db.Column(db.String(10))

    people = db.relationship('Person', backref='user', lazy='dynamic')
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic')
    categories = db.relationship('Category', backref='user', lazy='dynamic')

    def __repr__(self):
        return 'User {}'.format(self.user_id)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'login': self.login,
            'password': '*',
            'auth_key': self.auth_key,
            'transactions': [transaction.as_dict() for transaction in self.transactions]
        }

    @staticmethod
    def authenticate(user_id, auth_key):
        user = User.query.get(user_id)
        if user and user.auth_key == auth_key:
            return user
        return None


class Person(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    person_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    transactions = db.relationship('Transaction', backref='person', lazy='dynamic')
    transaction_items = db.relationship('TransactionItem', backref='person', lazy='dynamic')

    def __repr__(self):
        return '<Person {}>'.format(self.person_id)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'person_id': self.person_id,
            'name': self.name
        }


class Transaction(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    transaction_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, nullable=False)
    person_id = db.Column(db.Integer, nullable=False)
    transaction_date = db.Column(db.DateTime)
    value = db.Column(db.Float)
    notes = db.Column(db.String(500))
    type = db.Column(db.String(1))
    done = db.Column(db.Boolean)

    transaction_items = db.relationship('TransactionItem', backref='transaction', lazy='dynamic')

    __table_args__= (
        db.ForeignKeyConstraint(
            ['user_id', 'person_id'],
            ['person.user_id', 'person.person_id']
        ),
        db.ForeignKeyConstraint(
            ['user_id', 'category_id'],
            ['category.user_id', 'category.category_id']
        )
    )

    def __repr__(self):
        return '<Transaction {}.{}>'.format(self.user_id, self.transaction_id)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'transaction_id': self.transaction_id,
            'category_id': self.category_id,
            'person_id': self.person_id,
            'transaction_date': self.transaction_date,
            'value': self.value,
            'notes': self.notes,
            'type': self.type,
            'done': self.done,
            'person': self.person.as_dict(),
            'category': self.category.as_dict(),
            'transaction_items': [item.as_dict() for item in self.transaction_items]
        }


class TransactionItem(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, nullable=False)
    item_date = db.Column(db.DateTime)
    value = db.Column(db.Float)
    notes = db.Column(db.String(500))
    type = db.Column(db.String(1))
    done = db.Column(db.Boolean)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['user_id', 'transaction_id'],
            ['transaction.user_id', 'transaction.transaction_id']
        ),
        db.ForeignKeyConstraint(
            ['user_id', 'person_id'],
            ['person.user_id', 'person.person_id']
        )
    )

    def __repr__(self):
        return '<Transaction Item {}.{}.{}>'.format(self.user_id, self.transaction_id, self.item_id)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'transaction_id': self.transaction_id,
            'item_id': self.item_id,
            'person_id': self.person_id,
            'item_date': self.item_date,
            'value': self.value,
            'notes': self.notes,
            'type': self.type,
            'done': self.done
        }


class Category(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    icon_id = db.Column(db.Integer)

    transactions = db.relationship('Transaction', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<Category {}.{}>'.format(self.user_id, self.category_id)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'category_id': self.category_id,
            'name': self.name,
            'icon_id': self.icon_id
        }
