import arrow

from catherine.api import db
from sqlalchemy_utils import ArrowType


class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',
                           backref=db.backref('categories', lazy='dynamic'))

    def __init__(self, description, user, **kwargs):
        self.description = description
        self.user = user
        if 'icon' in kwargs:
            self.icon = kwargs['icon']

    def __repr__(self):
        return '<Category {}/{}>'.format(self.user.username, self.description)
