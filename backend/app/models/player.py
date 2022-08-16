from typing import Optional
from uuid import UUID

from sqlalchemy import UniqueConstraint, Sequence
from sqlmodel import Field, Relationship

from models import User
from models.base_model import AppBaseModel

seq = Sequence('golfer_id_seq', start=100000, maxvalue=900000, increment=1)


class Player(AppBaseModel, table=True):
    __table_args__ = (UniqueConstraint("golfer_id"),
                      UniqueConstraint("user_id"),
                      {'extend_existing': True})
    __mapper_args__ = {"eager_defaults": True}

    handicap: float = Field(default=None, nullable=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False, index=True)
    golfer_id: int = Field(nullable=False, default_factory=seq.next_value)

    user: Optional[User] = Relationship(back_populates='player')
