"""add_user_id_foreign_keys

Revision ID: 14bc8f85b4b7
Revises: 4fcc87813407
Create Date: 2024-01-21 18:13:51.629493

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "14bc8f85b4b7"
down_revision: Union[str, None] = "4fcc87813407"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Add user_id column to tags table
    op.add_column("tags", sa.Column("user_id", sa.VARCHAR(length=36)))

    # Create foreign keys
    op.create_foreign_key(None, "connections", "users", ["user_id"], ["id"])
    op.create_foreign_key(None, "tags", "users", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "tags", type_="foreignkey")
    op.drop_constraint(None, "connections", type_="foreignkey")
    op.drop_column("tags", "user_id")
    op.alter_column("connections", "user_id", type_=sa.VARCHAR(length=256))
    # ### end Alembic commands ###