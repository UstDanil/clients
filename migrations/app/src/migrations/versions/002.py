"""Add column creation_date to clients

Revision ID: 002
Revises: 001
Create Date: 2024-10-30 15:00:00

"""
from alembic import op
from datetime import datetime
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.text("ALTER TABLE clients ADD creation_date timestamp without time zone;"))
    op.execute(sa.text("UPDATE clients SET creation_date = NOW()"))
    op.execute(sa.text("ALTER TABLE clients ALTER COLUMN creation_date SET NOT NULL;"))


def downgrade() -> None:
    op.drop_column('clients', 'creation_date')
