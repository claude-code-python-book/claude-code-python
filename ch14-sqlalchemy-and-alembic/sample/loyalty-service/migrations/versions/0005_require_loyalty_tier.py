"""Make loyalty_accounts.tier NOT NULL without a long lock (contract).

Run this only once every running app version writes tier, and 0003 has
filled in the old rows. Each constraint is added NOT VALID, which needs only
a brief lock, then validated, which scans the table but lets reads and
writes continue. SET NOT NULL then uses the valid CHECK instead of scanning.

Revision ID: 0005
Revises: 0004
Create Date: 2026-11-16 09:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0005"
down_revision: str | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute(
            "ALTER TABLE loyalty_accounts ADD CONSTRAINT "
            "ck_loyalty_accounts_tier_not_null CHECK (tier IS NOT NULL) NOT VALID"
        )
        op.execute(
            "ALTER TABLE loyalty_accounts "
            "VALIDATE CONSTRAINT ck_loyalty_accounts_tier_not_null"
        )
        op.execute(
            "ALTER TABLE loyalty_accounts ADD CONSTRAINT "
            "ck_loyalty_accounts_tier_is_known "
            "CHECK (tier IN ('bronze', 'silver', 'gold')) NOT VALID"
        )
        op.execute(
            "ALTER TABLE loyalty_accounts "
            "VALIDATE CONSTRAINT ck_loyalty_accounts_tier_is_known"
        )
    op.alter_column(
        "loyalty_accounts",
        "tier",
        existing_type=sa.String(length=10),
        nullable=False,
        server_default="bronze",
    )
    op.drop_constraint(
        "ck_loyalty_accounts_tier_not_null", "loyalty_accounts", type_="check"
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_loyalty_accounts_tier_is_known", "loyalty_accounts", type_="check"
    )
    op.alter_column(
        "loyalty_accounts",
        "tier",
        existing_type=sa.String(length=10),
        nullable=True,
        server_default=None,
    )
