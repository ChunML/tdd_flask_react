import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user
from sqlalchemy.exc import IntegrityError


class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('chun', 'chun@email.com', 'password')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'chun')
        self.assertEqual(user.email, 'chun@email.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        add_user('chun', 'chun@email.com', 'password')
        duplicate_user = User(
            username='chun',
            email='chun2@email.com',
            password='password')
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user('chun', 'chun@email.com', 'password')
        duplicate_user = User(
            username='chun2',
            email='chun@email.com',
            password='password')
        db.session.add(duplicate_user)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_to_json(self):
        user = add_user('chun', 'chun@email.com', 'password')
        self.assertTrue(isinstance(user.to_json(), dict))

    def test_passwords_are_random(self):
        user_one = add_user('chun', 'chun@email.com', 'password')
        user_two = add_user('chun2', 'chun2@email.com', 'password')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        user = add_user('chun', 'chun@email.com', 'password')
        auth_token = user.encode_auth_token()
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user('chun', 'chun@email.com', 'password')
        auth_token = user.encode_auth_token()
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(User.decode_auth_token(auth_token), user.id)


if __name__ == '__main__':
    unittest.main()
