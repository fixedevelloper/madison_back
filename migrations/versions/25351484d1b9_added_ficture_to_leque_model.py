"""Added ficture to Leque model

Revision ID: 25351484d1b9
Revises: 738d67f2cfc8
Create Date: 2025-03-03 06:53:41.791539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25351484d1b9'
down_revision = '738d67f2cfc8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leagues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=242), nullable=True),
    sa.Column('logo', sa.String(length=242), nullable=True),
    sa.Column('type', sa.String(length=242), nullable=True),
    sa.Column('countryName', sa.String(length=242), nullable=True),
    sa.Column('countryCode', sa.String(length=242), nullable=True),
    sa.Column('is_favorite', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('leagues')
    # ### end Alembic commands ###
