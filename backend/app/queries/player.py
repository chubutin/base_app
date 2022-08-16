from uuid import UUID

from database import session_scope
from models import Player


def save_player(player: Player):
    with session_scope() as session:
        session.add(player)
        return player


def get_player_by_id(player_id: UUID):
    with session_scope() as session:
        return session.query(Player).filter_by(id=player_id).one()


def get_player_by_golfer_id(golfer_id):
    with session_scope() as session:
        return session.query(Player).filter_by(golfer_id=golfer_id).one()
