"""create posts table

Revision ID: e4f98b410ab2
Revises: 
Create Date: 2025-04-28 12:05:18.064817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4f98b410ab2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String, nullable=False),

    )



def downgrade() -> None:
    op.drop_table('posts')
    pass
