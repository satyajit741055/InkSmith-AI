"""add server_default to users created_at

Revision ID: 676c8346a5b5
Revises: 780188275f10
Create Date: 2026-08-02 21:41:59.461890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '676c8346a5b5'
down_revision: Union[str, Sequence[str], None] = '780188275f10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'users',
        'created_at',
        server_default=sa.text('now()'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'created_at', server_default=None)
