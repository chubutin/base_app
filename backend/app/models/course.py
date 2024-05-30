import sqlalchemy as sa

from models.base_model import AppBaseModel


class Course(AppBaseModel):
    __tablename__ = 'courses'

    datetime = sa.Column(sa.DateTime(timezone=True), nullable=False)
    address = sa.Column(sa.String, nullable=True)
