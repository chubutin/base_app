import random
import string
import uuid
from uuid import UUID

from models import User, Player

letters = string.ascii_lowercase


def get_random_lowercase():
    return "".join(random.choice(letters) for i in range(10))


def user_factory(username: str = None, email: str = None,
                 password: str= None, first_name: str = None, last_name: str = None,
                 disabled: bool = None, avatar_url: str = None):
    return User(username=username or f'fakeusername{get_random_lowercase()}',
                password=password or get_random_lowercase(),
                email=email or f'{get_random_lowercase()}@{get_random_lowercase()}.com',
                first_name=first_name or get_random_lowercase(),
                last_name=last_name or get_random_lowercase(),
                disabled=disabled or False,
                avatar_url=avatar_url or get_random_lowercase())


def player_factory(user_id: UUID = None, handicap: float = None):
    return Player(user_id=user_id or uuid.uuid4(),
                  handicap=handicap or 22.5)

