import json
from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import app
from models.user import User
from routers.users import authenticate_user
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

    def test_create_user_route_with_repeated_user__returns_error(self):
        user = UserFactory.build()
        # we save the password in another variable because  the password will get hashed
        password = user.password
        UserService.create_user(user)

        user_json = UserSchemaFactory.build(username=user.username, password=password)

        response = self.client.post("/users", json=json.loads(user_json.json()))
        self.assertEqual(400, response.status_code)
        self.assertEqual(response.json().get('detail'), 'Another user was created with that data')

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

    def test_activate_user_route(self):
        user = UserFactory.build()
        # we save the password in another variable because  the password will get hashed
        UserService.create_user(user)

        activate_url = f'/users/activate/?activation_code={user.hash_activation}'

        response = self.client.get(activate_url)

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response.json())
        self.assertEqual('User Activated', response.json()['message'])

    def test_activate_user_route__fails_wrong_activation_code(self):
        user = UserFactory.build()
        # we save the password in another variable because  the password will get hashed
        UserService.create_user(user)
        hash_activation_fake = 'fake_hash'

        activate_url = f'/users/activate/?activation_code={hash_activation_fake}'

        response = self.client.get(activate_url)

        self.assertEqual(400, response.status_code)
        self.assertIn(hash_activation_fake, response.json()['request'])


class TestAuthenticateUser(TestCase):

    def test_authenticate_user(self):
        user = UserFactory.build()
        # we save the password in another variable because  the password will get hashed
        password = user.password
        UserService.create_user(user)

        authenticated_user = authenticate_user(username=user.username, password=password)
        self.assertIsNotNone(authenticated_user)
        self.assertIsInstance(authenticated_user, User)

    def test_authenticate_user__username_not_exist__returns_none(self):
        self.assertFalse(authenticate_user(username='asdasd', password='asdasd'))

    def test_authenticate_user__incorrect_password__returns_none(self):
        user = UserFactory.build()
        UserService.create_user(user)
        self.assertFalse(authenticate_user(username=user.username, password='fakepassword'))
