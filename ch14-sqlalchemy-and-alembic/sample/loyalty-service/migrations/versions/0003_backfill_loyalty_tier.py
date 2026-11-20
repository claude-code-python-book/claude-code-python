"""Fill in loyalty_accounts.tier for existing accounts (data migration).

The thresholds are copied here, not imported from loyalty.rules: this
migration must do the same thing next year, whatever the rules say then.
Each batch commits on its own, so no lock is held for long. Needs a live
connection; it can't be rendered with --sql.

Revision ID: 0003
Revises: 0002
Create Date: 2026-11-09 09:40:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BATCH = 5_000
FILL_BATCH = sa.text("""
    UPDATE loyalty_accounts AS a
    SET tier = CASE
        WHEN s.spend >= 2000 THEN 'gold'
        WHEN s.spend >= 500 THEN 'silver'
        ELSE 'bronze'
    END
    FROM (
        SELECT la.customer_id, COALESCE(SUM(o.total), 0) AS spend
        FROM loyalty_accounts AS la
        LEFT JOIN orders AS o
            ON o.customer_id = la.customer_id
            AND o.placed_at > now() - interval '365 days'
        WHERE la.customer_id > :low AND la.customer_id <= :high
        GROUP BY la.customer_id
    ) AS s
    WHERE a.customer_id = s.customer_id AND a.tier IS NULL
""")


def upgrade() -> None:
    highest = op.get_bind().scalar(
        sa.text("SELECT max(customer_id) FROM loyalty_accounts")
    )
    with op.get_context().autocommit_block():
        for low in range(0, highest or 0, BATCH):
            op.execute(FILL_BATCH.bindparams(low=low, high=low + BATCH))


def downgrade() -> None:
    pass  # 0002's downgrade drops the column
