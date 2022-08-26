from typing import Optional

from pydantic import EmailStr

from app.schemas.base import AppBaseModelSchema


class UserExternalSchema(AppBaseModelSchema):

    username: str
    email: EmailStr
    first_name: str
    last_name: str
    disabled: bool = False
    avatar_url: Optional[str]
    activated: Optional[bool]


class UserSchema(UserExternalSchema):

    password: str
