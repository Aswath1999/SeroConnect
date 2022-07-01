"""empty message

Revision ID: e626cff8bffa
Revises: beb132fa4ba8
Create Date: 2022-06-27 17:57:09.719023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e626cff8bffa'
down_revision = 'beb132fa4ba8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('userimage', sa.String(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'userimage')
    # ### end Alembic commands ###