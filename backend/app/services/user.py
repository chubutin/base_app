import hashlib
from urllib.parse import urlparse, urlencode

from sqlalchemy.exc import NoResultFound

from auth import get_password_hash
from config.database import session_scope
from models.user import User
from services.main import AppService, AppCRUD
from utils.email import EmailSender, Email
from settings import Settings
from utils.errors import AppException

settings = Settings()


class UserService(AppService):

    @classmethod
    def create_user_activation_hash(cls, string_to_hash: str):
        hash_object = hashlib.sha1(string_to_hash.encode())
        return hash_object.hexdigest()

    @classmethod
    def create_user_activation_link(cls, activation_hash: str) -> str:
        params = {'code': activation_hash}
        base_url = urlparse(settings.base_activation_email_link)
        return base_url.geturl() + '?' + urlencode(params)

    @classmethod
    def create_user(cls, user: User):
        user.password = get_password_hash(user.password)
        user_created = UserCRUD.save_user(user)
        user.hash_activation = cls.create_user_activation_hash(user.username)
        cls.create_and_send_activation_email(user)
        return user_created

    @classmethod
    def create_and_send_activation_email(cls, user: User):
        email = Email(subject='Bienvenido a Golf App',
                      email_template=settings.email_template_name_user_activation,
                      email_variables={
                          'app_name': settings.appName,
                          'username': user.username,
                          'activation_link': cls.create_user_activation_link(user.hash_activation)
                      },
                      to=user.email)
        EmailSender().send(email)

    @classmethod
    def activate_user(cls, activation_code):
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


class UserCRUD(AppCRUD):

    @staticmethod
    def get_user_by_username(username: str):
        with session_scope() as session:
            return session.query(User).filter_by(username=username).one_or_none()

    @staticmethod
    def get_user_by_activation_code(activation_code: str):
        with session_scope() as session:
            return session.query(User).filter_by(hash_activation=activation_code).one_or_none()

    @staticmethod
    def save_user(user: User):
        with session_scope() as session:
            session.add(user)
            return user
