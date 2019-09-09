"""empty message

Revision ID: 59293be44865
Revises: 9ee97db0a2a9
Create Date: 2019-09-09 02:51:03.906454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59293be44865'
down_revision = '9ee97db0a2a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    # ### end Alembic commands ###
