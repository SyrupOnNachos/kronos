"""add_users_table

Revision ID: d874cf677b78
Revises: 6ccd3d350e34
Create Date: 2024-01-21 16:37:17.990873

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = "d874cf677b78"
down_revision: Union[str, None] = "6ccd3d350e34"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    inspector = Inspector.from_engine(op.get_bind())

    if "users" not in inspector.get_table_names():
        op.create_table(
            "users",
            sa.Column(
                "id",
                sa.VARCHAR(length=36),
                primary_key=True,
                autoincrement=False,
                nullable=False,
            ),
            sa.Column("username", sa.String(256), unique=True),
            sa.Column("email", sa.String(256), unique=True),
            sa.Column("password", sa.String),
            sa.Column(
                "created_on",
                sa.DateTime(timezone=True),
                server_default=sa.func.current_timestamp(),
            ),
            sa.Column(
                "updated_on",
                sa.DateTime(timezone=True),
                server_default=sa.func.current_timestamp(),
                onupdate=sa.func.current_timestamp(),
            ),
        )


# ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
