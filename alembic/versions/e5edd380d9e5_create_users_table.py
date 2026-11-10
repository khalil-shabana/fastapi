"""create users table

Revision ID: e5edd380d9e5
Revises: 5f7a74fcc430
Create Date: 2026-11-08 16:02:41.484995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5edd380d9e5'
down_revision: Union[str, Sequence[str], None] = '5f7a74fcc430'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
        # ...other columns
    )


def downgrade() -> None:
    op.drop_table("users")
