"""add content to posts table

Revision ID: 7cc3e7e4b39c
Revises: e4f98b410ab2
Create Date: 2025-04-28 12:23:12.144572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7cc3e7e4b39c'
down_revision: Union[str, None] = 'e4f98b410ab2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_column('posts', 'content')

