"""add_followers_table

Revision ID: ebde763d9a9f
Revises: 654ef9782dcd
Create Date: 2024-08-25 19:25:20.010846

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ebde763d9a9f'
down_revision = '654ef9782dcd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'followers',
        sa.Column('follower_id', sa.Integer(), nullable=False),
        sa.Column('followed_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['follower_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )


def downgrade():
    op.drop_table('followers')
