"""Initial migration.

Revision ID: bcf9df78e66b
Revises: 
Create Date: 2025-01-17 11:54:14.790808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcf9df78e66b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('api_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('region', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('api_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('api_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('height', sa.Float(), nullable=False),
    sa.Column('weight', sa.Float(), nullable=False),
    sa.Column('sprite', sa.String(), nullable=False),
    sa.Column('type_one', sa.String(), nullable=False),
    sa.Column('type_two', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('api_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('location_area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('api_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('api_id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('pokemon_location_area_table',
    sa.Column('pokemon_id', sa.Integer(), nullable=True),
    sa.Column('location_area_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['location_area_id'], ['location_area.id'], ),
    sa.ForeignKeyConstraint(['pokemon_id'], ['pokemon.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemon_location_area_table')
    op.drop_table('location_area')
    op.drop_table('pokemon')
    op.drop_table('location')
    # ### end Alembic commands ###
