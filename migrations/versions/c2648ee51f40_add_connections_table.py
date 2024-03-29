"""add_connections_table

Revision ID: c2648ee51f40
Revises: ab2fd3936d06
Create Date: 2024-01-16 15:15:56.281190

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = "c2648ee51f40"
down_revision: Union[str, None] = "ab2fd3936d06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    inspector = Inspector.from_engine(op.get_bind())

    if "connections" not in inspector.get_table_names():
        op.create_table(
            "connections",
            sa.Column("id", sa.VARCHAR(length=36), primary_key=True, autoincrement=False, nullable=False),
            sa.Column("user_id", sa.VARCHAR(length=36), nullable=False),
            sa.Column("service", sa.VARCHAR(length=256), nullable=False),
            sa.Column("auth_token", sa.VARCHAR(length=256)),
            sa.Column("created_on", sa.DateTime(), default=sa.func.current_timestamp()),
            sa.Column("expires_on", sa.DateTime()),
            sa.Column("meta_data", sa.VARCHAR()),
        )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("connections")
    # ### end Alembic commands ###
