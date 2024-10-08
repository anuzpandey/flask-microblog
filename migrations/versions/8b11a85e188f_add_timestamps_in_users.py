"""add_timestamps_in_users

Revision ID: 8b11a85e188f
Revises: cd4f40863a28
Create Date: 2024-08-01 01:07:47.927445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b11a85e188f'
down_revision = 'cd4f40863a28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_created_at'), ['created_at'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_updated_at'), ['updated_at'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_updated_at'))
        batch_op.drop_index(batch_op.f('ix_user_created_at'))
        batch_op.drop_column('updated_at')
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
