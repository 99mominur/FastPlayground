"""create user table

Revision ID: 3f0a8a2aa72a
Revises: 7cc3e7e4b39c
Create Date: 2025-05-05 17:51:43.252402

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3f0a8a2aa72a"
down_revision: Union[str, None] = "7cc3e7e4b39c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
