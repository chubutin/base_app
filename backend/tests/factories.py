import string

import factory
import faker
from factory.alchemy import SQLAlchemyModelFactory
from pydantic_factories import ModelFactory, Ignore

from models.user import User
from models.player import Player
from schemas.user import UserSchema

letters = string.ascii_lowercase

# MODELS FACTORIES WITH FACTORY BOY #

fake = faker.Faker()


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User

    username = factory.LazyFunction(fake.email)
    email = factory.LazyFunction(fake.email)
    first_name = fake.name()
    last_name = fake.last_name()
    disabled = False
    avatar_url = None
    activated = False
    password = factory.LazyFunction(fake.password)
    hash_activation = factory.LazyFunction(fake.text)


class PlayerFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Player

    user = factory.SubFactory(UserFactory)


# SCHEMA FACTORIES WITH PYDANTIC-FACTORIES #

class AppBaseModelFactory(ModelFactory):
    id = Ignore()
    created = Ignore()
    updated = Ignore()


class UserSchemaFactory(AppBaseModelFactory):
    __model__ = UserSchema
