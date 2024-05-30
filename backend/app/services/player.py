from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from models.player import Player
from services import AppCRUD, AppService


class PlayerService(AppService):

    def __init__(self, session: Optional[Session] = None):
        super(PlayerService, self).__init__()
        self.dao = PlayerCRUD(session)

    def save_player(self, player: Player):
        return self.dao.save_player(player)

    def get_player_by_user_id(self, user_id: UUID):
        return self.dao.get_player_by_user_id(user_id)


class PlayerCRUD(AppCRUD):

    def save_player(self, player: Player):
        self.session.add(player)
        return player

    def get_player_by_id(self, player_id: UUID):
        return self.session.query(Player).filter_by(id=player_id).one_or_none()

    def get_player_by_user_id(self, user_id):
        return self.session.query(Player).filter_by(user_id=user_id).one_or_none()
