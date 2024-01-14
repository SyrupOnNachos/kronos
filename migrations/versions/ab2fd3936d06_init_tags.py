"""init_tags

Revision ID: ab2fd3936d06
Revises: 
Create Date: 2024-01-14 11:26:28.348027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector
from snowflake.sqlalchemy import VARIANT

# revision identifiers, used by Alembic.
revision: str = 'ab2fd3936d06'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create an inspector object to inspect the database
    inspector = Inspector.from_engine(op.get_bind())

    # Check if the 'tags' table exists
    if 'tags' not in inspector.get_table_names():
        # If the table does not exist, create it with the VARIANT type for api_payload
        op.create_table('tags',
            sa.Column('id', sa.VARCHAR(length=36), autoincrement=False, nullable=False),
            sa.Column('tag_alias', sa.VARCHAR(length=256), nullable=False),
            sa.Column('description', sa.VARCHAR(length=16777216), nullable=True),
            sa.Column('api_payload', sa.VARCHAR(length=16777216), nullable=False),
            sa.PrimaryKeyConstraint('id', name='SYS_CONSTRAINT_eab11994-8539-4655-a735-2ac3a7d2e635')
        )

def downgrade() -> None:
    op.drop_table('tags')
