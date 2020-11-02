"""empty message

Revision ID: b42ab9aa2554
Revises: 
Create Date: 2020-11-02 19:15:31.996782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b42ab9aa2554'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('languages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=True),
    sa.Column('description', sa.String(length=120), nullable=True),
    sa.Column('image', sa.String(length=40), nullable=True),
    sa.Column('key', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    op.create_table('useradm',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=20), nullable=True),
    sa.Column('subtitle', sa.String(length=30), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('key', sa.String(length=20), nullable=True),
    sa.Column('exercise', sa.Text(), nullable=True),
    sa.Column('languageKey', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['languageKey'], ['languages.key'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('useradm')
    op.drop_table('languages')
    # ### end Alembic commands ###