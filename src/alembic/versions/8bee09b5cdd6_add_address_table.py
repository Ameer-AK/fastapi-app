"""add address table

Revision ID: 8bee09b5cdd6
Revises: ffa92163988e
Create Date: 2020-12-27 12:28:52.815182

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '8bee09b5cdd6'
down_revision = 'ffa92163988e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('address',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, primary_key=True),
    sa.Column('customer_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('street', sa.String(length=50), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('country', sa.String(length=50), nullable=True),
    )


def downgrade():
    op.drop_table('address')
