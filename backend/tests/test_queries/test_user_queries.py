from unittest import TestCase

from tests.factories import user_factory
from errors import IntegrityErrorException
from queries.user import save_user, get_user_by_username


class TestUserQueries(TestCase):

    def test_create_user(self):
        user = user_factory()
        user_db = save_user(user)
        self.assertIsNotNone(user_db)

    def test_create_user_with_same_username_raise_integrity_error(self):
        user = user_factory()
        save_user(user)
        duplicated_user = user_factory(username=user.username)
        with self.assertRaises(IntegrityErrorException):
            save_user(duplicated_user)

    def test_create_user_with_same_email_raise_integrity_error(self):
        user = user_factory()
        save_user(user)
        duplicated_user = user_factory(email=user.email)
        with self.assertRaises(IntegrityErrorException):
            save_user(duplicated_user)

    def test_create_user_with_null_first_name_fails(self):
        user = user_factory()
        user.first_name = None
        with self.assertRaises(IntegrityErrorException):
            save_user(user)

    def test_create_user_with_null_last_name_fails(self):
        user = user_factory()
        user.last_name = None
        with self.assertRaises(IntegrityErrorException):
            save_user(user)

    def test_create_user_with_null_email_fails(self):
        user = user_factory()
        user.email = None
        with self.assertRaises(IntegrityErrorException):
            save_user(user)

    def test_create_user_with_null_username_fails(self):
        user = user_factory()
        user.username = None
        with self.assertRaises(IntegrityErrorException):
            save_user(user)

    def test_get_user_by_username(self):
        user = user_factory()
        user_db = save_user(user)

        get_user_by_username(username=user.username)
        self.assertEqual(user, user_db)


