"""empty message

Revision ID: 9bd2af46bee5
Revises: 1ec946d2f02a
Create Date: 2024-07-31 01:41:39.331839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bd2af46bee5'
down_revision = '1ec946d2f02a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pet', schema=None) as batch_op:
        batch_op.drop_constraint('pet_breed_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pet', schema=None) as batch_op:
        batch_op.create_unique_constraint('pet_breed_key', ['breed'])

    # ### end Alembic commands ###