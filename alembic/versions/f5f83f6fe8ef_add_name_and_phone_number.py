"""add name and phone_number

Revision ID: f5f83f6fe8ef
Revises: cd2208e4dacd
Create Date: 2022-11-09 21:26:58.355518

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5f83f6fe8ef'
down_revision = 'cd2208e4dacd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('name', sa.String(), nullable = False))
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable = True))


def downgrade() -> None:
    op.drop_column('users', 'name')
    op.drop_column('users', 'phone_number')
