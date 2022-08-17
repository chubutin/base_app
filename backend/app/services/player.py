from uuid import UUID

from config.database import session_scope
from models.player import Player


class PlayerService:

    @staticmethod
    def save_player(player: Player):
        PlayerCRUD.save_player(player)

    @staticmethod
    def get_player_by_user_id(user_id: UUID):
        PlayerCRUD.get_player_by_user_id(user_id)


class PlayerCRUD:

    @staticmethod
    def save_player(player: Player):
        with session_scope() as session:
            session.add(player)
            return player

    @staticmethod
    def get_player_by_id(player_id: UUID):
        with session_scope() as session:
            return session.query(Player).filter_by(id=player_id).one()

    @staticmethod
    def get_player_by_golfer_id(golfer_id):
        with session_scope() as session:
            return session.query(Player).filter_by(golfer_id=golfer_id).one()

    @staticmethod
    def get_player_by_user_id(user_id):
        with session_scope() as session:
            return session.query(Player).filter_by(user_id=user_id).one()
