import sqlalchemy as sa
from sqlalchemy import Sequence
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from config.database import Base
from models.base_model import AppBaseModel

golfer_id_seq = Sequence('golfer_id_seq', minvalue=100000, maxvalue=500000, start=100000, metadata=Base.metadata)

class Player(AppBaseModel):
    __tablename__ = 'player'
    __table_args__ = (sa.UniqueConstraint("golfer_id"),
                      sa.UniqueConstraint("user_id"))

    field_seq_golfer_id = sa.Sequence('golfer_id_seq', start=100000, maxvalue=900000, increment=1)
    handicap = sa.Column('handicap', sa.Float, nullable=True)
    user_id = sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey("user.id"), nullable=False, index=True)
    golfer_id = sa.Column('golfer_id', sa.Integer, server_default=sa.FetchedValue(), nullable=False)

    user = relationship('User')
