from typing import Optional

from app.schemas.base import AppBaseModelSchema


class UserExternalSchema(AppBaseModelSchema):

    username: str
    email: str
    first_name: str
    last_name: str
    disabled: bool = False
    avatar_url: Optional[str]


class UserSchema(UserExternalSchema):

    password: str
