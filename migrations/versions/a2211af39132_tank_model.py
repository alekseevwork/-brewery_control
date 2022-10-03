"""Tank model

Revision ID: a2211af39132
Revises: ca414346879e
Create Date: 2022-10-02 18:52:09.328121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2211af39132'
down_revision = 'ca414346879e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tank',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=50), nullable=False),
    sa.Column('title', sa.Enum('kellerbier', 'dunkelbier', 'bropils', 'wheatbeer', 'traditional_dark', 'traditional_light', 'traditional_wheat', 'cider', name='titlebeer'), nullable=False),
    sa.Column('yeast', sa.String(length=50), nullable=False),
    sa.Column('actual_volume', sa.Integer(), nullable=True),
    sa.Column('beer_grooving', sa.Boolean(), nullable=True),
    sa.Column('cooling', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('measuring',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('temperature', sa.Float(), nullable=False),
    sa.Column('density', sa.Float(), nullable=False),
    sa.Column('pressure', sa.Float(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=False),
    sa.Column('comment', sa.String(length=300), nullable=True),
    sa.Column('tank_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tank_id'], ['tank.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_measuring_tank_id'), 'measuring', ['tank_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_measuring_tank_id'), table_name='measuring')
    op.drop_table('measuring')
    op.drop_table('tank')
    # ### end Alembic commands ###