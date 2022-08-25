import json
from datetime import timedelta
from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import app
from auth import create_access_token
from routers.users import create_dict_for_access_token
from tests.factories import UserSchemaFactory, UserFactory
from services.user import UserService


class TestUsersRouters(TestCase):

    def setUp(self) -> None:
        super(TestUsersRouters, self).setUp()
        self.client = TestClient(app)

    def test_authentication_endpoint(self):
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
        self.assertIsNotNone(response.json()['access_token'])

    def test_authentication_endpoint_with_wrong_password(self):
        user = UserFactory.build()
        # we save the password in another variable because  the password will get hashed
        UserService.create_user(user)

        authentication_payload = {
            'username': user.username,
            'password': 'fake_password'
        }
        response = self.client.post("/token", data=authentication_payload)

        self.assertEqual(401, response.status_code)

    def test_endpoint_with_expired_token__returns_401(self):
        user = UserFactory.build()
        # we save the password in another variable because  the password will get hashed
        UserService.create_user(user)

        access_token = create_access_token(data=create_dict_for_access_token(username=user.username),
                                           expires_delta=timedelta(-1, 1080))

        authorization_header = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get('/users/me', headers=authorization_header)

        self.assertEqual(401, response.status_code)

    def test_endpoint_with_null_user__returns_401(self):
        access_token = create_access_token(data={'fake_data': 'fake_value'})

        authorization_header = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get('/users/me', headers=authorization_header)

        self.assertEqual(401, response.status_code)

    def test_endpoint_with_valid_token_user_not_exists_returns_401(self):
        access_token = create_access_token(data=create_dict_for_access_token(username='fake_username'))

        authorization_header = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get('/users/me', headers=authorization_header)

        self.assertEqual(401, response.status_code)

    def test_endpoint_with_disabled_user(self):
        user = UserFactory.build()
        user.disabled = True
        # we save the password in another variable because  the password will get hashed
        UserService.create_user(user)

        access_token = create_access_token(data=create_dict_for_access_token(username=user.username))
        authorization_header = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get('/users/me', headers=authorization_header)

        self.assertEqual(400, response.status_code)
        self.assertEqual('Inactive user', response.json().get('detail'))
