from catherine.api import db


class TargetType(db.Model):

    __tablename__ = 'target_types'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(50), nullable=False)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return '<TargetType: {}>'.format(self.description)


class Target(db.Model):

    __tablename__ = 'targets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), nullable=False)

    target_type_id = db.Column(db.Integer, db.ForeignKey('target_types.id'))
    target_type = db.relationship(
        'TargetType', backref=db.backref('targets', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(
        'User', backref=db.backref('targets', lazy='dynamic'))

    def __init__(self, description, target_type, user):
        self.description = description
        self.target_type = target_type
        self.user = user

    def __repr__(self):
        return '<TargetType: {}>'.format(self.description)
