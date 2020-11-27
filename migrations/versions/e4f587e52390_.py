"""empty message

Revision ID: e4f587e52390
Revises: 675a24e5a75f
Create Date: 2020-11-20 23:33:15.500928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4f587e52390'
down_revision = '675a24e5a75f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('posts_ibfk_1', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'languages', ['languageKey'], ['key'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_ibfk_1', 'posts', 'languages', ['languageKey'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###