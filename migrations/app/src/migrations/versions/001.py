"""Create matches table

Revision ID: 001
Revises: 000
Create Date: 2024-10-30 10:00:00

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = '000'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('matches',
                    sa.Column('initiator_id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
                    sa.Column('client_id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
                    sa.ForeignKeyConstraint(['initiator_id'], ['clients.id']),
                    sa.ForeignKeyConstraint(['client_id'], ['clients.id']))
    op.create_index("initiator_id_matches_index", "matches", ["initiator_id"])
    op.create_index("client_id_matches_index", "matches", ["client_id"])


def downgrade() -> None:
    op.drop_index("initiator_id_matches_index")
    op.drop_index("client_id_matches_index")
    op.drop_table('matches')
