from unittest import TestCase

from services.user import UserService
from services.player import PlayerCRUD
from tests.factories import UserFactory, PlayerFactory
from utils.errors import IntegrityErrorException


class TestPlayerCRUD(TestCase):

    def test_create_player(self):
        user = UserFactory.build()
        player = PlayerFactory.build()
        player.user = user
        player_db = PlayerCRUD.save_player(player)
        self.assertIsNotNone(player_db)

    def test_create_second_player_with_same_user_raises_exception(self):
        user = UserFactory.build()
        UserService.create_user(user)
        player = PlayerFactory.build()
        player.user = user
        player_db = PlayerCRUD.save_player(player)
        self.assertIsNotNone(player_db)
        player = PlayerFactory.build()
        player.user = user

        with self.assertRaises(IntegrityErrorException):
            PlayerCRUD.save_player(player)




