import sqlalchemy as sa

from auth import get_password_hash
from models.base_model import AppBaseModel


class User(AppBaseModel):
    __tablename__ = 'user'
    __table_args__ = (sa.UniqueConstraint("username"),
                      sa.UniqueConstraint("email")
                      )
    username = sa.Column(sa.String, nullable=False, index=True)
    email = sa.Column(sa.String, nullable=False, index=True)
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    disabled = sa.Column(sa.Boolean, default=False, nullable=False)
    avatar_url = sa.Column(sa.String, default=None, nullable=True)
    password = sa.Column(sa.String, nullable=False)
    activated = sa.Column(sa.Boolean, default=False, nullable=False)
    hash_activation = sa.Column(sa.String, nullable=True)
    reset_password_hash = sa.Column(sa.String, nullable=True)

    def generate_reset_password_hash(self):
        self.reset_password_hash = get_password_hash(password=f'{self.email}_{self.password}')
