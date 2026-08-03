"""prompt size removed

Revision ID: e5bf8559ddd2
Revises: 676c8346a5b5
Create Date: 2026-08-03 18:21:41.862957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5bf8559ddd2'
down_revision: Union[str, Sequence[str], None] = '676c8346a5b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
