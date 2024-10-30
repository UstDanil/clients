"""Add columns latitude and longitude to clients

Revision ID: 003
Revises: 002
Create Date: 2024-10-30 18:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.text("ALTER TABLE clients ADD latitude decimal;"))
    op.execute(sa.text("UPDATE clients SET latitude = 55.4424"))
    op.execute(sa.text("ALTER TABLE clients ADD longitude decimal;"))
    op.execute(sa.text("UPDATE clients SET longitude = 37.3636"))
    op.execute(sa.text("ALTER TABLE clients ALTER COLUMN latitude SET NOT NULL;"))
    op.execute(sa.text("ALTER TABLE clients ALTER COLUMN longitude SET NOT NULL;"))


def downgrade() -> None:
    op.drop_column('clients', 'longitude')
    op.drop_column('clients', 'latitude')
