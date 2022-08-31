from abc import ABC

from config.database import session_scope
from utils.errors import DatabaseException


class AppService:
    pass


class AppCRUD(ABC):

    mapped_class = None

    def filter_by(self, **kwargs):
        try:
            with session_scope() as session:
                return session.query(self.mapped_class).filter_by(**kwargs).all()
        except Exception as exc:
            raise DatabaseException(exc)
