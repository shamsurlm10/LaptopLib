"""Created a new column balance with default value 10000

Revision ID: 7353f72f1da5
Revises: 
Create Date: 2022-12-31 16:59:30.963151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7353f72f1da5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('balance', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('balance')

    # ### end Alembic commands ###