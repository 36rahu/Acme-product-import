"""empty message

Revision ID: 0f13e6d8b6c6
Revises: bae5d7fd7d95
Create Date: 2019-08-30 02:02:04.999040

"""

# revision identifiers, used by Alembic.
revision = '0f13e6d8b6c6'
down_revision = 'bae5d7fd7d95'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('webhooks',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('event', sa.VARCHAR(length=64), nullable=False),
    sa.Column('endpoint', sa.VARCHAR(length=64), nullable=False),
    sa.Column('extra_paylod', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Webhooks')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Webhooks',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Webhooks_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('event', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('endpoint', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('extra_paylod', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Webhooks_pkey')
    )
    op.drop_table('webhooks')
    # ### end Alembic commands ###
