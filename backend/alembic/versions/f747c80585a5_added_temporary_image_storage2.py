"""added temporary image storage2

Revision ID: f747c80585a5
Revises: 1e0cf2126488
Create Date: 2025-11-25 06:49:51.819339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f747c80585a5'
down_revision: Union[str, Sequence[str], None] = '1e0cf2126488'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
