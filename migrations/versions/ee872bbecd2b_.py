"""empty message

Revision ID: ee872bbecd2b
Revises: d6779fe0e672
Create Date: 2022-08-07 23:09:36.486308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee872bbecd2b'
down_revision = 'd6779fe0e672'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('website', sa.String(length=250), nullable=True))
    op.add_column('artist', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('artist', sa.Column('seeking_description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'seeking_description')
    op.drop_column('artist', 'seeking_talent')
    op.drop_column('artist', 'website')
    # ### end Alembic commands ###
