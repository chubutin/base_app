from abc import ABC
from typing import Optional

from sqlalchemy.orm import Session

from utils.database import SessionLocal
from utils.errors import DatabaseException


class AppCRUD:

    mapped_class = None

    def __init__(self, session: Optional[Session] = None):
        self.session = session or SessionLocal()

    def filter_by(self, **kwargs):
        try:
            return self.session.query(self.mapped_class).filter_by(**kwargs).all()
        except Exception as exc:
            raise DatabaseException(exc)


class AppService:
    pass
