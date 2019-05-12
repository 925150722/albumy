"""add collect

Revision ID: 829afba037b6
Revises: 9b70ea144ed2
Create Date: 2019-05-06 15:49:50.424482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '829afba037b6'
down_revision = '9b70ea144ed2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('collect',
    sa.Column('collector_id', sa.Integer(), nullable=False),
    sa.Column('collected_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['collected_id'], ['photo.id'], ),
    sa.ForeignKeyConstraint(['collector_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('collector_id', 'collected_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('collect')
    # ### end Alembic commands ###
