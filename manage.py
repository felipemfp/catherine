#!/usr/bin/env python

import os
import unittest
import coverage
import getpass

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from catherine.api import app, db

COV = coverage.coverage(
    branch=True,
    include='catherine/api/*',
    omit=[
        'catherine/tests/*',
        'catherine/api/config.py',
        'catherine/api/*/__init__.py'
    ]
)
COV.start()

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('catherine/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('catherine/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def check():
    """Checks source code for errors."""
    os.system('pyflakes catherine')


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_data():
    """Creates sample data."""
    from catherine.api.targets.models import TargetType
    db.session.add(TargetType('Pessoa'))
    db.session.add(TargetType('Estabelecimento'))
    db.session.commit()


@manager.command
def create_user():
    """Creates user."""
    from catherine.api.auth.models import User
    username = input('Username: ').strip()
    password = getpass.getpass('Password: ')
    user = User(username, password=password)
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
