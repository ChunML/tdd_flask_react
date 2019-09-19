import json
import unittest
from flask import current_app
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        response = self.client.post(
            '/auth/register',
            data=json.dumps({
                'username': 'chun',
                'email': 'chun@email.com',
                'password': '123456'
            }),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        add_user('chun', 'chun@email.com', '123456')
        response = self.client.post(
            '/auth/register',
            data=json.dumps({
                'username': 'chun2',
                'email': 'chun@email.com',
                'password': '123456'
            }),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Sorry. That user already exists.', data['message'])
        self.assertIn('fail', data['status'])

    def test_user_registration_duplicate_username(self):
        add_user('chun', 'chun@email.com', '123456')
        response = self.client.post(
            '/auth/register',
            data=json.dumps({
                'username': 'chun',
                'email': 'chun2@email.com',
                'password': '123456'
            }),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Sorry. That user already exists.', data['message'])
        self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json(self):
        response = self.client.post(
            '/auth/register',
            data=json.dumps({}),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_username(self):
        response = self.client.post(
            '/auth/register',
            data=json.dumps({
                'email': 'chun@email.com',
                'password': '123456'
            }),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_email(self):
        response = self.client.post(
            '/auth/register',
            data=json.dumps({
                'username': 'chun',
                'password': '123456'
            }),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_user_registration_invalid_json_keys_no_password(self):
        response = self.client.post(
            '/auth/register',
            data=json.dumps({
                'username': 'chun',
                'email': 'chun@email.com'
            }),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_registered_user_login(self):
        add_user('chun', 'chun@email.com', 'password')
        response = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'chun@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertIn('success', data['status'])
        self.assertIn('Successfully logged in.', data['message'])
        self.assertTrue(data['auth_token'])
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_not_registered_user_login(self):
        response = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'chun@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertIn('fail', data['status'])
        self.assertIn('User does not exist.', data['message'])
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 404)

    def test_valid_logout(self):
        add_user('chun', 'chun@email.com', 'password')
        response = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'chun@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        auth_token = json.loads(response.data.decode())['auth_token']
        response = self.client.get(
            '/auth/logout',
            headers={'Authorization': f'Bearer {auth_token}'})
        data = json.loads(response.data.decode())
        self.assertIn('success', data['status'])
        self.assertIn('Successfully logged out.', data['message'])
        self.assertEqual(response.status_code, 200)

    def test_invalid_logout_expired_token(self):
        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
        add_user('chun', 'chun@email.com', 'password')
        response = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'chun@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        auth_token = json.loads(response.data.decode())['auth_token']
        response = self.client.get(
            '/auth/logout',
            headers={'Authorization': f'Bearer {auth_token}'})
        data = json.loads(response.data.decode())
        self.assertIn('fail', data['status'])
        self.assertIn(
            'Signature expired. Please log in again.', data['message'])
        self.assertEqual(response.status_code, 401)

    def test_invalid_logout(self):
        response = self.client.get(
            '/auth/logout',
            headers={'Authorization': f'Bearer invalid'})
        data = json.loads(response.data.decode())
        self.assertIn('fail', data['status'])
        self.assertIn(
            'Invalid token. Please log in again.', data['message'])
        self.assertEqual(response.status_code, 401)

    def test_user_status(self):
        add_user('chun', 'chun@email.com', 'password')
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'chun@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        token = json.loads(resp_login.data.decode())['auth_token']
        response = self.client.get(
            '/auth/status',
            headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data.decode())
        self.assertIn('success', data['status'])
        self.assertIsNotNone(data['data'])
        self.assertEqual('chun', data['data']['username'])
        self.assertEqual('chun@email.com', data['data']['email'])
        self.assertTrue(data['data']['active'])
        self.assertFalse(data['data']['admin'])
        self.assertEqual(response.status_code, 200)

    def test_invalid_status(self):
        response = self.client.get(
            '/auth/status',
            headers={'Authorization': f'Bearer invalid'})
        data = json.loads(response.data.decode())
        self.assertIn('fail', data['status'])
        self.assertIn(
            'Invalid token. Please log in again.', data['message'])
        self.assertEqual(response.status_code, 401)

    def test_invalid_logout_inactive(self):
        add_user('chun', 'chun@email.com', 'password')
        user = User.query.filter_by(email='chun@email.com').first()
        user.active = False
        db.session.commit()
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'chun@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        token = json.loads(resp_login.data.decode())['auth_token']
        response = self.client.get(
            '/auth/logout',
            headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data.decode())
        self.assertIn('fail', data['status'])
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertEqual(response.status_code, 401)

    def test_invalid_status_inactive(self):
        add_user('chun', 'chun@email.com', 'password')
        user = User.query.filter_by(email='chun@email.com').first()
        user.active = False
        db.session.commit()
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'chun@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        token = json.loads(resp_login.data.decode())['auth_token']
        response = self.client.get(
            '/auth/status',
            headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data.decode())
        self.assertIn('fail', data['status'])
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
