"""add server_default to created_at and updated_at

Revision ID: 780188275f10
Revises: 07650de6dd05
Create Date: 2026-08-02 21:38:50.317154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '780188275f10'
down_revision: Union[str, Sequence[str], None] = '07650de6dd05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'blog_generations',
        'created_at',
        server_default=sa.text('now()'),
    )
    op.alter_column(
        'blog_generations',
        'updated_at',
        server_default=sa.text('now()'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('blog_generations', 'created_at', server_default=None)
    op.alter_column('blog_generations', 'updated_at', server_default=None)