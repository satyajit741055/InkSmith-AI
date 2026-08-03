"""add current_step column to blog_generations

Revision ID: 5fb73547cbd4
Revises: 53f1fc11ba95
Create Date: 2026-08-03 21:53:50.073091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5fb73547cbd4'
down_revision: Union[str, Sequence[str], None] = '53f1fc11ba95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('blog_generations', sa.Column('current_step', sa.String(length=255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('blog_generations', 'current_step')
