from unittest import TestCase
from unittest.mock import patch

import faker

from services.user import UserCRUD, UserService
from settings import Settings
from tests.factories import UserFactory
from utils.email import get_email_template_by_name
from utils.errors import IntegrityErrorException, AppException

settings = Settings()


class TestUserService(TestCase):
    
    def setUp(self) -> None:
        self.fake = faker.Faker()
        super(TestUserService, self).setUp()

    def test_create_user_activation_hash(self):
        username = 'fake_username'
        self.assertIsNotNone(UserService.create_user_activation_hash(username))

    def test_create_user_activation_hash_is_idempotent(self):
        username = 'fake_username'
        self.assertEqual(UserService.create_user_activation_hash(username),
                         UserService.create_user_activation_hash(username))

    def test_create_user(self):
        user = UserFactory.build()
        UserService.create_user(user)

    def test_create_user_assert_activation_email_is_send(self):
        with patch('app.services.user.EmailSender.send') as send_mock:
            user = UserFactory.build()
            UserService.create_user(user)
            send_mock.assert_called()

    def test_create_and_send_activation_email(self):
        with patch('app.services.user.EmailSender.send') as send_mock:
            user = UserFactory.build()
            UserService.create_and_send_activation_email(user)
            send_mock.assert_called_once()
            email_argument,  = send_mock.call_args_list[0][0]
            self.assertEqual(email_argument.subject, 'Bienvenido a Golf App')
            self.assertEqual(email_argument.to, user.email)
            self.assertEqual(email_argument.content,
                             get_email_template_by_name(settings.email_template_name_user_activation))

    def test_activate_user(self):
        hash_activation = self.fake.text()
        user = UserFactory.build()
        user.hash_activation = hash_activation
        UserService.create_user(user)
        UserService.activate_user(hash_activation)

        user_db = UserCRUD.get_user_by_username(user.username)
        self.assertTrue(user_db)

    def test_activate_user_fails_if_not_user_with_activation_code(self):
        hash_activation = self.fake.text()
        user = UserFactory.build()
        user.hash_activation = 'fake_hash_123'
        UserService.create_user(user)

        with self.assertRaises(AppException) as exc_info:
            UserService.activate_user(hash_activation)
            self.assertEqual(exc_info.value.args[0], 'Activation Code is not valid')

    def test_activate_user_fails_if_user_is_activated(self):
        hash_activation = self.fake.text()
        user = UserFactory.build()
        user.hash_activation = hash_activation
        user.activated = True
        UserService.create_user(user)

        with self.assertRaises(AppException) as exc_info:
            UserService.activate_user(hash_activation)
            self.assertEqual(exc_info.value.args[0], 'User is already activated')

    def test_activate_user_fails_if_user_is_disabled(self):
        user = UserFactory.build()
        user.activated = False
        user.disabled = True
        UserService.create_user(user)

        with self.assertRaises(AppException) as exc_info:
            UserService.activate_user(user.hash_activation)
            self.assertEqual(exc_info.value.args[0], 'User is deactivated')


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


