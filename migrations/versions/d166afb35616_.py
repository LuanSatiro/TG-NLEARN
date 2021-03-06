"""empty message

Revision ID: d166afb35616
Revises: 84a561d3176a
Create Date: 2020-11-20 23:00:16.855655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd166afb35616'
down_revision = '84a561d3176a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('posts_ibfk_1', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'languages', ['languageKey'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_ibfk_1', 'posts', 'languages', ['languageKey'], ['key'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###
