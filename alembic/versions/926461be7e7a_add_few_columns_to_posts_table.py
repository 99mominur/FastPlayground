"""add few columns to posts table

Revision ID: 926461be7e7a
Revises: c99f10955dfe
Create Date: 2025-05-05 18:50:21.857376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '926461be7e7a'
down_revision: Union[str, None] = 'c99f10955dfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean, server_default='TRUE', nullable=False),
    )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
