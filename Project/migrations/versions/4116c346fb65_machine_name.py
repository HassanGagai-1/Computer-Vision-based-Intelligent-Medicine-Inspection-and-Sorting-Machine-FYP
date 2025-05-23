"""machine name

Revision ID: 4116c346fb65
Revises: 64aa13839664
Create Date: 2025-01-29 14:59:55.621711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4116c346fb65'
down_revision = '64aa13839664'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('machine', schema=None) as batch_op:
        batch_op.add_column(sa.Column('machine_name', sa.String(length=255), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('machine', schema=None) as batch_op:
        batch_op.drop_column('machine_name')

    # ### end Alembic commands ###
