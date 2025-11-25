"""added temporary image storage

Revision ID: 1e0cf2126488
Revises: c53af81c3dbf
Create Date: 2025-11-25 06:45:04.596389

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e0cf2126488'
down_revision: Union[str, Sequence[str], None] = 'c53af81c3dbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
