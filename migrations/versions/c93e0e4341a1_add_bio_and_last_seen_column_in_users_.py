"""add_bio_and_last_seen_column_in_users_table

Revision ID: c93e0e4341a1
Revises: b0dfe13e9de8
Create Date: 2024-08-05 00:00:53.001244

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c93e0e4341a1'
down_revision = 'b0dfe13e9de8'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bio', sa.String(length=256), nullable=True))
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_seen')
        batch_op.drop_column('bio')
