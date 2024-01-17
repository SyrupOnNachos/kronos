"""update_tags_rename_action_script_column_and_add_created_on

Revision ID: 6ccd3d350e34
Revises: c2648ee51f40
Create Date: 2024-01-16 15:35:21.240856

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6ccd3d350e34"
down_revision: Union[str, None] = "c2648ee51f40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename column 'api_payload' to 'action_script'
    op.execute("ALTER TABLE tags RENAME COLUMN api_payload TO action_script")

    # Add 'created_on' column with the current timestamp as the default value
    op.add_column(
        "tags",
        sa.Column("created_on", sa.DateTime(), default=sa.func.current_timestamp()),
    )


def downgrade() -> None:
    # Rename column 'action_script' back to 'api_payload'
    op.execute("ALTER TABLE tags RENAME COLUMN action_script TO api_payload")

    # Remove the 'created_on' column
    op.drop_column("tags", "created_on")
