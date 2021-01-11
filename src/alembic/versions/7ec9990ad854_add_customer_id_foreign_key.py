"""add customer_id foreign key

Revision ID: 7ec9990ad854
Revises: 8bee09b5cdd6
Create Date: 2020-12-27 12:30:05.719916

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '7ec9990ad854'
down_revision = '8bee09b5cdd6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key("fk_customer_address", "address",
                          "customer", ["customer_id"], ["id"])


def downgrade():
    op.drop_constraint("fk_customer_address", "address")
