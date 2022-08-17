from auth import get_password_hash
from config.database import session_scope
from models.user import User
from services.main import AppService, AppCRUD


class UserService(AppService):

    @staticmethod
    def create_user(user: User):
        user.password = get_password_hash(user.password)
        return UserCRUD.save_user(user)


class UserCRUD(AppCRUD):

    @staticmethod
    def get_user_by_username(username: str):
        with session_scope() as session:
            return session.query(User).filter_by(username=username).one()

    @staticmethod
    def save_user(user: User):
        with session_scope() as session:
            session.add(user)
            return user
