from catherine.api import db


class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',
                           backref=db.backref('categories', lazy='dynamic'))

    def __init__(self, description, user):
        self.description = description
        self.user = user

    def __repr__(self):
        return '<Category: {}/{}>'.format(self.user.username, self.description)
