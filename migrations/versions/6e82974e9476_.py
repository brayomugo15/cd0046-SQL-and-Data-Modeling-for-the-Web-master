"""empty message

Revision ID: 6e82974e9476
Revises: 0fb9032f10d9
Create Date: 2022-08-10 00:28:39.557211

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6e82974e9476'
down_revision = '0fb9032f10d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('start_time', sa.DateTime(), nullable=False))
    op.drop_column('show', 'start_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('start_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_column('show', 'start_time')
    # ### end Alembic commands ###
