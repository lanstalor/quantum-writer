"""Initial tables"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'stories',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('genre', sa.String(length=100)),
        sa.Column('description', sa.Text()),
        sa.Column('story_metadata', sa.JSON()),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )
    op.create_table(
        'branches',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('story_id', sa.String(), nullable=False),
        sa.Column('parent_branch_id', sa.String()),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('is_main', sa.Boolean(), default=False),
        sa.Column('status', sa.String(length=50), default='active'),
        sa.Column('branch_metadata', sa.JSON()),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )
    op.create_table(
        'chapters',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('story_id', sa.String(), nullable=False),
        sa.Column('branch_id', sa.String()),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.Column('word_count', sa.Integer(), default=0),
        sa.Column('chapter_metadata', sa.JSON()),
        sa.Column('version', sa.Integer(), default=1),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )
    op.create_table(
        'characters',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('story_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('role', sa.String(length=100)),
        sa.Column('traits', sa.JSON()),
        sa.Column('relationships', sa.JSON()),
        sa.Column('arc', sa.Text()),
        sa.Column('embedding_id', sa.String()),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('updated_at', sa.DateTime(timezone=True)),
    )

def downgrade():
    op.drop_table('characters')
    op.drop_table('chapters')
    op.drop_table('branches')
    op.drop_table('stories')
