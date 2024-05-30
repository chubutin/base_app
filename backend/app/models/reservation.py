import sqlalchemy as sa
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from utils.database import Base
from models.base_model import AppBaseModel

players_reservations_table = Table(
    "players_reservations",
    Base.metadata,
    sa.Column("player_id", sa.ForeignKey("players.id"), index=True),
    sa.Column("reservation_id", sa.ForeignKey("reservations.id"), index=True),
)


class Reservation(AppBaseModel):
    __tablename__ = 'reservations'

    datetime = sa.Column(sa.DateTime(timezone=True), nullable=False)
    players = relationship("Player", secondary=players_reservations_table)
    anonymous_players = sa.ARRAY(sa.String())
    course_id = sa.Column('course_id', sa.String, nullable=False)
