"""first setup

Revision ID: 2c18758bcbd9
Revises: 
Create Date: 2019-10-03 20:42:28.693511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c18758bcbd9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('director',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('extras', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_director_name'), 'director', ['name'], unique=True)
    op.create_table('movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('star', sa.String(length=64), nullable=True),
    sa.Column('genre', sa.String(length=64), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('recommended', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(length=256), nullable=True),
    sa.Column('director_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['director_id'], ['director.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movie_genre'), 'movie', ['genre'], unique=False)
    op.create_index(op.f('ix_movie_star'), 'movie', ['star'], unique=False)
    op.create_index(op.f('ix_movie_title'), 'movie', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_movie_title'), table_name='movie')
    op.drop_index(op.f('ix_movie_star'), table_name='movie')
    op.drop_index(op.f('ix_movie_genre'), table_name='movie')
    op.drop_table('movie')
    op.drop_index(op.f('ix_director_name'), table_name='director')
    op.drop_table('director')
    # ### end Alembic commands ###
