from unittest import TestCase

from tests.factories import user_factory, player_factory
from errors import IntegrityErrorException
from queries.player import save_player
from queries.user import save_user


class TestUserQueries(TestCase):

    def test_create_player(self):
        user = user_factory()
        user_db = save_user(user)
        player = player_factory(user_id=user_db.id)
        player_db = save_player(player)
        self.assertIsNotNone(player_db)

    def test_create_second_player_with_same_user_raises_exception(self):
        user = user_factory()
        user_db = save_user(user)
        player = player_factory(user_id=user_db.id)
        player_db = save_player(player)
        self.assertIsNotNone(player_db)
        player = player_factory(user_id=user_db.id)

        with self.assertRaises(IntegrityErrorException):
            save_player(player)




