"""questionnaire added

Revision ID: 0afa754e1c5f
Revises: 00d929031ee2
Create Date: 2024-06-11 10:31:35.501987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0afa754e1c5f'
down_revision = '00d929031ee2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questionnaire',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('personal_info', sa.Integer(), nullable=False),
    sa.Column('pet', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['personal_info'], ['personal_info.id'], ),
    sa.ForeignKeyConstraint(['pet'], ['pet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('personal_info', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'personal_info', ['personal_info'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('personal_info')

    op.drop_table('questionnaire')
    # ### end Alembic commands ###