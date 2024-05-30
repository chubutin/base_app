import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base_model import AppBaseModel


class Player(AppBaseModel):
    __tablename__ = 'players'

    user_id = sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False, index=True)
    handicap_score = sa.Column('handicap', sa.Float)
    handicap_id = sa.Column('handicap_id', sa.Integer)
    user = relationship('User')
