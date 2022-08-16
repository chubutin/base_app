import uuid
from datetime import datetime

from uuid import UUID

from sqlmodel import SQLModel, Field


class AppBaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid.uuid4, nullable=False, index=True, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


