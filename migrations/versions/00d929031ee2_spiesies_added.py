"""spiesies added

Revision ID: 00d929031ee2
Revises: c80292e1ff3b
Create Date: 2024-06-11 10:24:04.509171

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '00d929031ee2'
down_revision = 'c80292e1ff3b'
branch_labels = None
depends_on = None

# Enum definitions
petgender = postgresql.ENUM('MALE', 'FEMALE', 'OTHER', name='petgender')
petsize = postgresql.ENUM('SMALL', 'MEDIUM', 'LARGE', name='petsize')


def upgrade():
    # Create the enums
    petgender.create(op.get_bind())
    petsize.create(op.get_bind())

    # Alter the pet table to add the new columns
    with op.batch_alter_table('pet', schema=None) as batch_op:
        batch_op.add_column(sa.Column('gender', petgender, nullable=False))
        batch_op.add_column(sa.Column('size', petsize, nullable=False))
        batch_op.add_column(sa.Column('species_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'species', ['species_id'], ['id'])


def downgrade():
    # Drop the pet table columns
    with op.batch_alter_table('pet', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('species_id')
        batch_op.drop_column('size')
        batch_op.drop_column('gender')

    # Drop the enums
    petgender.drop(op.get_bind())
    petsize.drop(op.get_bind())
