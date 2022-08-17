import json
from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import app
from tests.factories import UserSchemaFactory, UserFactory
from services.user import UserService


class TestTokenRouters(TestCase):

    def setUp(self) -> None:
        super(TestTokenRouters, self).setUp()
        self.client = TestClient(app)

    def test_auth_route(self):
        user = UserFactory.build()
        # we save the password in another variable because  the password will get hashed
        password = user.password
        UserService.create_user(user)
        authentication_payload = {
            'username': user.username,
            'password': password
        }
        response = self.client.post("/token", data=authentication_payload)
        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json())
        self.assertIsNotNone(response.json()['access_token'])


class TestUsersRouters(TestCase):
    
    def setUp(self) -> None:
        super(TestUsersRouters, self).setUp()
        self.client = TestClient(app)

    def test_create_user_route(self):
        user_json = UserSchemaFactory.build()
        response = self.client.post("/users", json=json.loads(user_json.json()))
        self.assertEqual(200, response.status_code)
        user_response = response.json()
        self.assertIsNotNone(user_response)
        self.assertIsNotNone(user_response['id'])

    def test_users_me_route(self):
        user = UserFactory.build()
        # we save the password in another variable because  the password will get hashed
        password = user.password
        UserService.create_user(user)
        authentication_payload = {
            'username': user.username,
            'password': password
        }
        response = self.client.post("/token", data=authentication_payload)
        access_token = response.json()['access_token']

        authorization_header = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get('/users/me', headers=authorization_header)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json())
        self.assertEqual(str(user.id), response.json()['id'])


