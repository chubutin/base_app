import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AppBaseModelSchema(BaseModel):

    id: Optional[uuid.UUID]
    created: Optional[datetime]
    updated: Optional[datetime]
