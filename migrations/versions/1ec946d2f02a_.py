"""empty message

Revision ID: 1ec946d2f02a
Revises: 
Create Date: 2024-07-31 01:39:13.696542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ec946d2f02a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('personal_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=120), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('species',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'AVAILABLE', 'ADOPTED', 'BOOKED', name='petstatus'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('pet',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('breed', sa.String(length=80), nullable=True),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', 'OTHER', name='petgender'), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('is_sterilized', sa.Boolean(), nullable=False),
    sa.Column('size', sa.Enum('SMALL', 'MEDIUM', 'LARGE', name='petsize'), nullable=False),
    sa.Column('species_id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.String(length=90), nullable=True),
    sa.Column('image', sa.String(length=300), nullable=True),
    sa.Column('description', sa.String(length=300), nullable=True),
    sa.Column('status', sa.Enum('PENDING', 'AVAILABLE', 'ADOPTED', 'BOOKED', name='petstatus'), nullable=True),
    sa.ForeignKeyConstraint(['species_id'], ['species.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('breed'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=254), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=True),
    sa.Column('personal_info_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['personal_info_id'], ['personal_info.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('questionnaire',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('personal_info_id', sa.Integer(), nullable=False),
    sa.Column('pet_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['personal_info_id'], ['personal_info.id'], ),
    sa.ForeignKeyConstraint(['pet_id'], ['pet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('questionnaire')
    op.drop_table('user')
    op.drop_table('pet')
    op.drop_table('species')
    op.drop_table('personal_info')
    # ### end Alembic commands ###
