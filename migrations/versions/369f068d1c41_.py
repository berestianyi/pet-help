"""empty message

Revision ID: 369f068d1c41
Revises: a4b08d979c88
Create Date: 2024-06-13 12:20:36.797057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '369f068d1c41'
down_revision = 'a4b08d979c88'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('breed', sa.String(length=80), nullable=True))
        batch_op.create_unique_constraint(None, ['breed'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pet', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('breed')

    # ### end Alembic commands ###