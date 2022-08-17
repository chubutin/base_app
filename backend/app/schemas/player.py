from typing import Optional

from app.schemas.base import AppBaseModelSchema
from schemas.user import UserExternalSchema


class PlayerSchema(AppBaseModelSchema):

    handicap: Optional[float]
    user: UserExternalSchema
    golfer_id: int
