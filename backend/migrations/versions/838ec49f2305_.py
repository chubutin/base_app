"""empty message

Revision ID: 838ec49f2305
Revises: 
Create Date: 2023-03-21 03:04:35.539394

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '838ec49f2305'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reservations',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=False),
    sa.Column('datetime', sa.DateTime(timezone=True), nullable=False),
    sa.Column('course_id', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('disabled', sa.Boolean(), nullable=False),
    sa.Column('avatar_url', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('activated', sa.Boolean(), nullable=False),
    sa.Column('hash_activation', sa.String(), nullable=True),
    sa.Column('reset_password_hash', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('players',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated', sa.DateTime(timezone=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('handicap', sa.Float(), nullable=True),
    sa.Column('handicap_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_players_user_id'), 'players', ['user_id'], unique=False)
    op.create_table('players_reservations',
    sa.Column('player_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('reservation_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['players.id'], ),
    sa.ForeignKeyConstraint(['reservation_id'], ['reservations.id'], )
    )
    op.create_index(op.f('ix_players_reservations_player_id'), 'players_reservations', ['player_id'], unique=False)
    op.create_index(op.f('ix_players_reservations_reservation_id'), 'players_reservations', ['reservation_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_players_reservations_reservation_id'), table_name='players_reservations')
    op.drop_index(op.f('ix_players_reservations_player_id'), table_name='players_reservations')
    op.drop_table('players_reservations')
    op.drop_index(op.f('ix_players_user_id'), table_name='players')
    op.drop_table('players')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('reservations')
    # ### end Alembic commands ###
