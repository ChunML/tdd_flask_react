from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User
import unittest
import sys


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db():
    db.session.add(User(username='trung', email='chun@email.com'))
    db.session.add(User(username='nguyen', email='nguyen@email.com'))
    db.session.commit()


@cli.command()
def test():
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


if __name__ == '__main__':
    cli()
