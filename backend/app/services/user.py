import hashlib
from typing import Optional
from urllib.parse import urlparse, urlencode

from sqlalchemy.orm import Session

from auth import get_password_hash
from models.user import User
from services.main import AppService, AppCRUD
from settings import Settings
from utils.email import EmailSender, Email
from utils.errors import AppException

settings = Settings()


class UserCRUD(AppCRUD):

    def __init__(self, session: Session = None):
        super().__init__(session)
        self.mapped_class = User

    def get_user_by_username(self, username: str):
        return self.session.query(User).filter_by(username=username).one_or_none()

    def get_user_by_email(self, email: str):
        return self.session.query(User).filter_by(email=email).one_or_none()

    def get_user_by_activation_code(self, activation_code: str):
        return self.session.query(User).filter_by(hash_activation=activation_code).one_or_none()

    def save_user(self, user: User):
        self.session.add(user)
        return user


class UserService(AppService):

    def __init__(self, session:  Optional[Session] = None):
        super(UserService, self).__init__()
        self.dao = UserCRUD(session)

    @staticmethod
    def create_user_activation_hash(string_to_hash: str):
        hash_object = hashlib.sha1(string_to_hash.encode())
        return hash_object.hexdigest()

    @staticmethod
    def create_user_activation_link(activation_hash: str) -> str:
        params = {'code': activation_hash}
        base_url = urlparse(settings.base_activation_email_link)
        return base_url.geturl() + '?' + urlencode(params)

    @staticmethod
    def create_reset_password_link(reset_password_hash: str) -> str:
        params = {'token': reset_password_hash}
        base_url = urlparse(settings.base_activation_email_link)
        return base_url.geturl() + '?' + urlencode(params)

    def create_user(self, user: User):
        user.password = get_password_hash(user.password)
        user.hash_activation = self.create_user_activation_hash(user.username)
        user_created = self.dao.save_user(user)
        self.create_and_send_activation_email(user)
        return user_created

    def create_and_send_activation_email(self, user: User):
        email = Email(subject='Bienvenido a Golf App',
                      email_template=settings.email_template_name_user_activation,
                      email_variables={
                          'app_name': settings.appName,
                          'username': user.username,
                          'activation_link': self.create_user_activation_link(user.hash_activation)
                      },
                      to=user.email)
        EmailSender().send(email)

    def create_and_send_reset_password_email(self, user: User):
        email = Email(subject=f'Hello {user.first_name}',
                      email_template=settings.email_template_name_reset_password,
                      email_variables={
                          'firstname': user.first_name,
                          'reset_password_link': self.create_reset_password_link(user.reset_password_hash)
                      },
                      to=user.email)
        EmailSender().send(email)

    @classmethod
    def initialize_reset_password_and_send_email(self, email: str):
        try:
            user = UserCRUD.get_user_by_email(email=email)
            if user:
                user.generate_reset_password_hash()
                UserCRUD.save_user(user)
                self.create_and_send_reset_password_email(user)
        except Exception as exc:
            raise AppException(exc)

    @classmethod
    def activate_user(self, activation_code):
        user = UserCRUD.get_user_by_activation_code(activation_code)
        if not user:
            raise AppException('Activation Code is not valid')
        if user.activated:
            raise AppException('User is already activated')
        if user.disabled:
            raise AppException('User is deactivated')
        user.activated = True
        user.hash_activation = None
        UserCRUD.save_user(user)


