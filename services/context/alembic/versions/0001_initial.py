"""Initial tables"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'story_contexts',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('story_id', sa.String(), nullable=False, unique=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

def downgrade():
    op.drop_table('story_contexts')
