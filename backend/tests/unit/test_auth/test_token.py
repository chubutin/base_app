from datetime import timedelta
from unittest import TestCase
from jose import jwt, ExpiredSignatureError

from app.auth.token import create_access_token
from settings import Settings


class TestCreateAccessToken(TestCase):

    def test_create_access_token(self):
        self.assertIsNotNone(create_access_token({'username': 'username'}))

    def test_create_access_token_with_expiration_date(self):
        delta = timedelta(-1, 1080)
        self.assertIsNotNone(create_access_token({'username': 'username'},
                                                 expires_delta=delta))

    def test_create_access_token_no_expiration_date_jwt_is_valid(self):
        token = create_access_token({'username': 'username'})
        jwt.decode(token, key=Settings().secret_key, algorithms=Settings().algorithm)

    def test_create_access_token_with_expiration_date__assert_is_valid(self):
        delta = timedelta(1080)

        access_token = create_access_token({'username': 'username'}, expires_delta=delta)

        jwt.decode(access_token, key=Settings().secret_key, algorithms=Settings().algorithm)

    def test_create_access_token_with_expiration_date_negative__assert_is_expired(self):
        delta = timedelta(-1, 1080)

        access_token = create_access_token({'username': 'username'}, expires_delta=delta)

        with self.assertRaises(ExpiredSignatureError):
            jwt.decode(access_token, key=Settings().secret_key, algorithms=Settings().algorithm)



