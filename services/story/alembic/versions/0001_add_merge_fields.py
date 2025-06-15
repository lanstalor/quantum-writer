"""add merge fields to branch

Revision ID: 0001_add_merge_fields
Revises: 
Create Date: 2024-01-01
"""

from alembic import op
import sqlalchemy as sa

revision = '0001_add_merge_fields'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('branches', sa.Column('merged_into_id', sa.String(), nullable=True))
    op.add_column('branches', sa.Column('merged_at', sa.DateTime(timezone=True), nullable=True))

def downgrade():
    op.drop_column('branches', 'merged_at')
    op.drop_column('branches', 'merged_into_id')
