from unittest import TestCase

from services.user import UserCRUD
from tests.factories import UserFactory
from utils.errors import IntegrityErrorException


class TestUserCRUD(TestCase):

    def test_create_user(self):
        user = UserFactory.build()
        user_db = UserCRUD.save_user(user)
        self.assertIsNotNone(user_db)

    def test_create_user_with_same_username_raise_integrity_error(self):
        user = UserFactory.build()
        UserCRUD.save_user(user)
        duplicated_user = UserFactory.build(username=user.username)
        with self.assertRaises(IntegrityErrorException):
            UserCRUD.save_user(duplicated_user)

    def test_create_user_with_same_email_raise_integrity_error(self):
        user = UserFactory.build()
        UserCRUD.save_user(user)
        duplicated_user = UserFactory.build(email=user.email)
        with self.assertRaises(IntegrityErrorException):
            UserCRUD.save_user(duplicated_user)

    def test_create_user_with_null_first_name_fails(self):
        user = UserFactory.build()
        user.first_name = None
        with self.assertRaises(IntegrityErrorException):
            UserCRUD.save_user(user)

    def test_create_user_with_null_last_name_fails(self):
        user = UserFactory.build()
        user.last_name = None
        with self.assertRaises(IntegrityErrorException):
            UserCRUD.save_user(user)

    def test_create_user_with_null_email_fails(self):
        user = UserFactory.build()
        user.email = None
        with self.assertRaises(IntegrityErrorException):
            UserCRUD.save_user(user)

    def test_create_user_with_null_username_fails(self):
        user = UserFactory.build()
        user.username = None
        with self.assertRaises(IntegrityErrorException):
            UserCRUD.save_user(user)

    def test_get_user_by_username(self):
        user = UserFactory.build()
        user_db = UserCRUD.save_user(user)

        UserCRUD.get_user_by_username(username=user.username)
        self.assertEqual(user, user_db)


