"""add featured flag to projects

Revision ID: 7b14df2964d1
Revises: 261fea5cb716
Create Date: 2026-09-24 14:43:02.259296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7b14df2964d1"
down_revision: Union[str, Sequence[str], None] = "261fea5cb716"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "projects",
        sa.Column(
            "is_featured",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.alter_column(
        "projects",
        "is_featured",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("projects", "is_featured")
