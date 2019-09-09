import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user
from sqlalchemy.exc import IntegrityError


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('chun', 'chun@email.com')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'chun')
        self.assertEqual(user.email, 'chun@email.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        add_user('chun', 'chun@email.com')
        duplicate_user = User(
            username='chun',
            email='chun2@email.com')
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user('chun', 'chun@email.com')
        duplicate_user = User(
            username='chun2',
            email='chun@email.com')
        db.session.add(duplicate_user)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_to_json(self):
        user = add_user('chun', 'chun@email.com')
        self.assertTrue(isinstance(user.to_json(), dict))


if __name__ == '__main__':
    unittest.main()
