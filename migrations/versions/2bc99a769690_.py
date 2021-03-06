"""empty message

Revision ID: 2bc99a769690
Revises: b9ea3d71d82a
Create Date: 2021-11-22 09:14:37.738730

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bc99a769690'
down_revision = 'b9ea3d71d82a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cms_member',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company', sa.String(length=100), nullable=True),
    sa.Column('position', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.String(length=11), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cms_member')
    # ### end Alembic commands ###
