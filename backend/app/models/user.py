from typing import Optional

from sqlmodel import Field, UniqueConstraint

from models.base_model import AppBaseModel


class UserExternal(AppBaseModel):
    """This class is used for user serialization only"""
    username: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, index=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    disabled: bool = Field(default=False, nullable=False)
    avatar_url: Optional[str] = Field(default=None, nullable=True)


class User(UserExternal, table=True):
    """This class is the Database User model"""
    __table_args__ = (UniqueConstraint("username"),
                      UniqueConstraint("email"),
                      {'extend_existing': True}
                      )
    password: str = Field(nullable=False)
