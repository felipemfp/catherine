import unittest
import time

from catherine.tests.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):

    def test_register_and_login(self):
        response = self.register('foobar', 'foobaz', 'Foo', 'Bar')
        self.assertStatus(response, 201)
        response = self.login('foobar', 'foobaz')
        self.assert200(response)
        self.assertIn('access_token', response.json.keys())

    def test_refresh(self):
        access_token = self.login_and_register('foobar', 'foobaz').json['access_token']
        time.sleep(1)

        response = self.client.post('/login/refresh/', data=dict(
            token=access_token
        ), follow_redirects=True)
        self.assert200(response)
        self.assertIn('access_token', response.json.keys())
        self.assertNotEqual(access_token, response.json['access_token'])

    def test_get_details(self):
        access_token = self.login_and_register('foobar', 'foobaz', 'Foo', 'Bar').json['access_token']

        response = self.client.get('/me/', headers={
            'Authorization': 'JWT {}'.format(access_token)
        })
        self.assert200(response)
        self.assertEqual('foobar', response.json['username'])
        self.assertEqual('Foo', response.json['first_name'])
        self.assertEqual('Bar', response.json['last_name'])

    def test_put_details(self):
        access_token = self.login_and_register('foobar', 'foobaz', 'Foo', 'Bar').json['access_token']

        response = self.client.put('/me/', headers={
            'Authorization': 'JWT {}'.format(access_token)
        }, data=dict(
            last_name='Baz'
        ))
        self.assert200(response)
        self.assertEqual('Baz', response.json['last_name'])

        response = self.client.put('/me/', headers={
            'Authorization': 'JWT {}'.format(access_token)
        }, data=dict(
            first_name='Joe'
        ))
        self.assert200(response)
        self.assertEqual('Joe', response.json['first_name'])

        response = self.client.put('/me/', headers={
            'Authorization': 'JWT {}'.format(access_token)
        }, data=dict(
            cur_password='foobaz',
            new_password='joebar'
        ))
        self.assert200(response)

        response = self.login('foobar', 'joebar')
        self.assert200(response)
        self.assertIn('access_token', response.json.keys())

    def test_delete(self):
        access_token = self.login_and_register('foobar', 'foobaz').json['access_token']
        response = self.client.delete('/me/', headers={
            'Authorization': 'JWT {}'.format(access_token)
        })
        self.assertStatus(response, 204)

    def test_login_method_not_allowed(self):
        response = self.client.get('/login/')
        self.assert405(response)


if __name__ == '__main__':
    unittest.main()
