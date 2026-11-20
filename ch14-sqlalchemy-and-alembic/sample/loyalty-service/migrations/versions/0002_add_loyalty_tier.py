"""Add loyalty_accounts.tier, nullable for now (expand).

The running app version doesn't know this column. The next version writes
it on every update; 0003 fills in the old rows; 0005 makes it NOT NULL.

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-09 09:30:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "loyalty_accounts", sa.Column("tier", sa.String(length=10), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("loyalty_accounts", "tier")
