from unittest import TestCase
import uuid

from services.player import PlayerCRUD, PlayerService
from tests.factories import UserFactory, PlayerFactory
from utils.errors import IntegrityErrorException


class TestPlayerService(TestCase):

    def test_create_player(self):
        user = UserFactory.build()
        player = PlayerFactory.build()
        player.user = user
        player_db = PlayerService.save_player(player)
        self.assertIsNotNone(player_db)

    def test_get_player_by_user_id(self):
        user = UserFactory.build()
        player = PlayerFactory.build()
        player.user = user
        player_db = PlayerCRUD.save_player(player)

        self.assertIsNotNone(PlayerService.get_player_by_user_id(player_db.user.id))


class TestPlayerCRUD(TestCase):

    def test_create_player(self):
        user = UserFactory.build()
        player = PlayerFactory.build()
        player.user = user
        player_db = PlayerCRUD.save_player(player)
        self.assertIsNotNone(player_db)

    def test_create_second_player_with_same_user_raises_exception(self):
        user = UserFactory.build()
        player = PlayerFactory.build()
        player.user = user
        player_db = PlayerCRUD.save_player(player)
        self.assertIsNotNone(player_db)
        player = PlayerFactory.build()
        player.user = user

        with self.assertRaises(IntegrityErrorException):
            PlayerCRUD.save_player(player)

    def test_get_player_by_id(self):
        user = UserFactory.build()
        player = PlayerFactory.build()
        player.user = user
        player_db = PlayerCRUD.save_player(player)
        self.assertIsNotNone(PlayerCRUD.get_player_by_id(player_db.id))

    def test_get_player_by_id_not_exist(self):
        self.assertIsNone(PlayerCRUD.get_player_by_id(uuid.uuid4()))

    def test_get_golfer_id(self):
        user = UserFactory.build()
        player = PlayerFactory.build()
        player.user = user
        player_db = PlayerCRUD.save_player(player)
        self.assertIsNotNone(PlayerCRUD.get_player_by_golfer_id(player_db.golfer_id))

    def test_get_player_by_golfer_id_not_exist(self):
        self.assertIsNone(PlayerCRUD.get_player_by_golfer_id(111111))

    def test_get_player_by_user_id(self):
        user = UserFactory.build()
        player = PlayerFactory.build()
        player.user = user
        PlayerCRUD.save_player(player)
        self.assertIsNotNone(PlayerCRUD.get_player_by_user_id(user.id))

    def test_get_player_by_user_id_not_exist(self):
        self.assertIsNone(PlayerCRUD.get_player_by_user_id(uuid.uuid4()))


