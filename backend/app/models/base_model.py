import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from utils.database import Base


class AppBaseModel(Base):
    """SQLAlchemy Base class for all database models."""
    __abstract__ = True

    id: UUID = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return str(self.__dict__)
