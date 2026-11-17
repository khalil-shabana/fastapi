"""make phone_num nullable

Revision ID: a3c1f9d27b64
Revises: 0be2aea4d3de
Create Date: 2026-11-16 14:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3c1f9d27b64'
down_revision: Union[str, Sequence[str], None] = '0be2aea4d3de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Databases that ran the previous migration while it still said
    # nullable=False need the constraint dropped; elsewhere this is a no-op.
    op.alter_column('users', 'phone_num', existing_type=sa.String(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    # Left nullable on purpose: restoring NOT NULL would fail on rows without a phone number.
    pass
