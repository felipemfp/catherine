import arrow

from catherine.api import app, db, bcrypt
from sqlalchemy_utils import ArrowType
from flask_login import UserMixin


class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(ArrowType, nullable=False)

    def __init__(self, username, **kwargs):
        self.username = username
        if 'password' in kwargs:
            self.set_password(kwargs['password'])
        if 'first_name' in kwargs:
            self.first_name = kwargs['first_name']
        if 'last_name' in kwargs:
            self.last_name = kwargs['last_name']
        self.created_at = arrow.utcnow()

    def check_password(self, password):
        if password is None:
            return False
        return bcrypt.check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        )
        return self.password

    def __repr__(self):
        return '<User {}>'.format(self.username)
