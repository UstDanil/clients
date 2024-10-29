"""Create clients table

Revision ID: 000
Revises:
Create Date: 2024-10-29 10:00:00

"""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table('clients',
                    sa.Column('id', postgresql.UUID(as_uuid=True), default=uuid4(), nullable=False),
                    sa.Column('gender', sa.String(), nullable=False),
                    sa.Column('first_name', sa.String(), nullable=False),
                    sa.Column('last_name', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('avatar', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'))
    op.create_unique_constraint('clients_email', 'clients', ['email'])

def downgrade() -> None:
    op.drop_table('clients')
