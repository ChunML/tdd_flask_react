import json
import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user, add_admin


class TestUserService(BaseTestCase):
    def test_users(self):
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        add_admin('test', 'test@email.com', 'password')
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'test@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        token = json.loads(resp_login.data.decode())['auth_token']
        response = self.client.post(
            '/users',
            data=json.dumps({
                'username': 'chun',
                'email': 'chun@email.com',
                'password': 'password'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('chun@email.com was added!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        add_admin('test', 'test@email.com', 'password')
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'test@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        token = json.loads(resp_login.data.decode())['auth_token']
        response = self.client.post(
            '/users',
            data=json.dumps({}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        add_admin('test', 'test@email.com', 'password')
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'test@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        token = json.loads(resp_login.data.decode())['auth_token']
        response = self.client.post(
            '/users',
            data=json.dumps({'email_and_name': 'chun@email.com'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys_no_password(self):
        add_admin('test', 'test@email.com', 'password')
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'test@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        token = json.loads(resp_login.data.decode())['auth_token']
        response = self.client.post(
            '/users',
            data=json.dumps({'email': 'chun@email.com'}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        add_admin('test', 'test@email.com', 'password')
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'test@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        token = json.loads(resp_login.data.decode())['auth_token']
        self.client.post(
            '/users',
            data=json.dumps({
                'username': 'chun',
                'email': 'chun@email.com',
                'password': 'password'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'})
        response = self.client.post(
            '/users',
            data=json.dumps({
                'username': 'chun',
                'email': 'chun@email.com',
                'password': 'password'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Sorry. That email already exists.', data['message'])
        self.assertIn('fail', data['status'])

    def test_single_user(self):
        user = add_user('chun', 'chun@email.com', 'password')
        response = self.client.get(f'/users/{user.id}')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('chun', data['data']['username'])
        self.assertIn('chun@email.com', data['data']['email'])
        self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        response = self.client.get('/users/blah')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertIn('User does not exist.', data['message'])
        self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        response = self.client.get('/users/999')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertIn('User does not exist.', data['message'])
        self.assertIn('fail', data['status'])

    def test_all_users(self):
        add_user('chun', 'chun@email.com', 'password')
        add_user('trung', 'trung@email.com', 'password')
        response = self.client.get('/users')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 2)
        self.assertIn('success', data['status'])
        self.assertIn('chun', data['data'][0]['username'])
        self.assertIn('chun@email.com', data['data'][0]['email'])
        self.assertTrue(data['data'][0]['active'])
        self.assertFalse(data['data'][0]['admin'])
        self.assertIn('trung', data['data'][1]['username'])
        self.assertIn('trung@email.com', data['data'][1]['email'])
        self.assertTrue(data['data'][1]['active'])
        self.assertFalse(data['data'][1]['admin'])

    def test_main_no_users(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('All Users', response.data.decode())
        self.assertIn('<p>No users!</p>', response.data.decode())

    def test_main_with_users(self):
        add_user('chun', 'chun@email.com', 'password')
        add_user('tran', 'tran@email.com', 'password')
        response = self.client.get('/')
        data = response.data.decode()
        self.assertEqual(response.status_code, 200)
        self.assertIn('All Users', data)
        self.assertNotIn('<p>No users!</p>', data)
        self.assertIn('chun', data)
        self.assertIn('tran', data)

    def test_main_add_user(self):
        response = self.client.post(
            '/',
            data=dict(
                username='chun',
                email='chun@email.com',
                password='password'),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        data = response.data.decode()
        self.assertIn('All Users', data)
        self.assertNotIn('<p>No users!</p>', data)
        self.assertIn('chun', data)

    def test_add_user_inactive(self):
        add_user('test', 'test@email.com', 'password')
        user = User.query.filter_by(email='test@email.com').first()
        user.active = False
        db.session.commit()
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'test@email.com',
                'password': 'password'
            }),
            content_type='application/json')
        token = json.loads(resp_login.data.decode())['auth_token']
        response = self.client.post(
            '/users',
            data=json.dumps({
                'username': 'chun',
                'email': 'chun@email.com',
                'password': 'password'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data.decode())
        self.assertIn('fail', data['status'])
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertEqual(response.status_code, 401)

    def test_add_user_not_admin(self):
        add_user('chun', 'chun@email.com', 'password')
        resp_login = self.client.post(
            '/auth/login',
            data=json.dumps({
                'email': 'chun@email.com',
                'password': 'password'
                }),
            content_type='application/json')
        token = json.loads(resp_login.data.decode())['auth_token']
        response = self.client.post(
            '/users',
            data=json.dumps({
                'username': 'test',
                'emai': 'test@email.com',
                'password': 'password'
                }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data.decode())
        self.assertIn('fail', data['status'])
        self.assertIn('You do not have the permission to do that.',
                      data['message'])
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
