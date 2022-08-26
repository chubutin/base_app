from unittest import TestCase

from pydantic import ValidationError

from schemas.user import UserSchema


class TestUserSchemas(TestCase):

    def test_create_user(self):
        UserSchema(username='username',
                   email='email@email.com',
                   first_name='name',
                   last_name='lastname',
                   disabled=False,
                   password='password123')

    def test_create_user_with_invalid_email(self):
        with self.assertRaises(ValidationError):
            UserSchema(username='username',
                       email='invalid_email',
                       first_name='name',
                       last_name='lastname',
                       disabled=False,
                       password='password123')
