"""add foreign key to posts table

Revision ID: c99f10955dfe
Revises: 3f0a8a2aa72a
Create Date: 2025-05-05 18:21:18.919638

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c99f10955dfe"
down_revision: Union[str, None] = "3f0a8a2aa72a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )
    op.create_foreign_key(
        "fk_posts_users",  # name of the foreign key constraint
        source_table="posts",  # source table
        referent_table="users",  # target table
        local_cols=["owner_id"],  # source column(s)
        remote_cols=["id"],  # target column(s)
        ondelete="CASCADE",  # action on delete
    )
    pass


def downgrade() -> None:
    op.drop_constraint("fk_posts_users", "posts", type_="foreignkey")
    op.drop_column("posts", "owner_id")
    pass
