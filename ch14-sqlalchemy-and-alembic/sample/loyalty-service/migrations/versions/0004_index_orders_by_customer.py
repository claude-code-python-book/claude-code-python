"""Index orders by customer and date, without blocking writes.

Revision ID: 0004
Revises: 0003
Create Date: 2026-11-09 10:00:00
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.create_index(
            "ix_orders_customer_placed",
            "orders",
            ["customer_id", "placed_at"],
            postgresql_concurrently=True,
        )


def downgrade() -> None:
    with op.get_context().autocommit_block():
        op.drop_index(
            "ix_orders_customer_placed",
            table_name="orders",
            postgresql_concurrently=True,
        )
