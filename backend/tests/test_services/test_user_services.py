from unittest import TestCase
from unittest.mock import patch

import faker

from services.user import UserCRUD, UserService
from settings import Settings
from tests.factories import UserFactory
from utils.email import get_email_template_by_name
from utils.errors import IntegrityErrorException, AppException, DatabaseException

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

    def test_initialize_reset_password_and_send_email(self):
        user = UserFactory.build()
        user.activated = False
        user.disabled = True
        UserService.create_user(user)

        with patch('app.services.user.EmailSender.send') as send_mock:
            UserService.initialize_reset_password_and_send_email(user.email)
            send_mock.assert_called()


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
        user = UserCRUD.save_user(user)

        user_retrieved = UserCRUD.get_user_by_username(username=user.username)
        self.assertEqual(user.id, user_retrieved.id)

    def test_get_filter_by_single_parameter(self):
        user = UserFactory.build()
        UserCRUD.save_user(user)

        filter_parameters = {'username': user.username}

        user_crud = UserCRUD()
        result = user_crud.filter_by(**filter_parameters)
        self.assertIsNotNone(result)
        self.assertNotEqual(result, [])

        self.assertEqual(user.id, result[0].id)

    def test_get_filter_by_single_parameter_with_wrong_filter(self):
        user = UserFactory.build()
        UserCRUD.save_user(user)

        filter_parameters = {'username': 'fake_username'}

        user_crud = UserCRUD()
        result = user_crud.filter_by(**filter_parameters)
        self.assertIsNotNone(result)
        self.assertEqual(result, [])

    def test_get_filter_by_multiple_parameters(self):
        user = UserFactory.build()
        UserCRUD.save_user(user)

        filter_parameters = {'username': user.username,
                             'email': user.email}

        user_crud = UserCRUD()
        result = user_crud.filter_by(**filter_parameters)
        self.assertIsNotNone(result)
        self.assertNotEqual(result, [])

        self.assertEqual(user.id, result[0].id)

    def test_get_filter_by_multiple_parameters_with_wrong_filter(self):
        user = UserFactory.build()
        UserCRUD.save_user(user)

        filter_parameters = {'username': user.username,
                             'email': 'fake_email'}

        user_crud = UserCRUD()
        result = user_crud.filter_by(**filter_parameters)
        self.assertIsNotNone(result)
        self.assertEqual(result, [])

    def test_get_filter_by_with_wrong_name_parameter(self):
        filter_parameters = {'fake_field': 'fake_value'}

        user_crud = UserCRUD()

        with self.assertRaises(DatabaseException):
            user_crud.filter_by(**filter_parameters)

    def test_get_filter_by_with_null_value_parameter(self):
        filter_parameters = {'username': None}

        user_crud = UserCRUD()

        result = user_crud.filter_by(**filter_parameters)
        self.assertIsNotNone(result)
        self.assertEqual(result, [])

