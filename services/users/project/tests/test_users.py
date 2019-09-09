import json
import unittest
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserService(BaseTestCase):
    def test_users(self):
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        response = self.client.post(
            '/users',
            data=json.dumps({
                'username': 'chun',
                'email': 'chun@email.com'
            }),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertIn('chun@email.com was added!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        response = self.client.post(
            '/users',
            data=json.dumps({}),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        response = self.client.post(
            '/users',
            data=json.dumps({'email': 'chun@email.com'}),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        self.client.post(
            '/users',
            data=json.dumps({
                'username': 'chun',
                'email': 'chun@email.com'
            }),
            content_type='application/json')

        response = self.client.post(
            '/users',
            data=json.dumps({
                'username': 'chun',
                'email': 'chun@email.com'
            }),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Sorry. That email already exists.', data['message'])
        self.assertIn('fail', data['status'])

    def test_single_user(self):
        user = add_user('chun', 'chun@email.com')
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
        add_user('chun', 'chun@email.com')
        add_user('trung', 'trung@email.com')
        response = self.client.get('/users')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 2)
        self.assertIn('success', data['status'])
        self.assertIn('chun', data['data'][0]['username'])
        self.assertIn('chun@email.com', data['data'][0]['email'])
        self.assertIn('trung', data['data'][1]['username'])
        self.assertIn('trung@email.com', data['data'][1]['email'])

    def test_main_no_users(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('All Users', response.data.decode())
        self.assertIn('<p>No users!</p>', response.data.decode())

    def test_main_with_users(self):
        add_user('chun', 'chun@email.com')
        add_user('tran', 'tran@email.com')
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
            data=dict(username='chun', email='chun@email.com'),
            follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        data = response.data.decode()
        self.assertIn('All Users', data)
        self.assertNotIn('<p>No users!</p>', data)
        self.assertIn('chun', data)


if __name__ == '__main__':
    unittest.main()
