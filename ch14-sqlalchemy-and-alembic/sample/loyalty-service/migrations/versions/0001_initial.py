"""Create customers, orders and the loyalty ledger.

Revision ID: 0001
Revises:
Create Date: 2026-11-02 10:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_customers")),
        sa.UniqueConstraint("email", name=op.f("uq_customers_email")),
    )
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("total", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column(
            "placed_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("total >= 0", name=op.f("ck_orders_total_not_negative")),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            name=op.f("fk_orders_customer_id_customers"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_orders")),
    )
    op.create_table(
        "loyalty_accounts",
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("balance", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "balance >= 0", name=op.f("ck_loyalty_accounts_balance_not_negative")
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customers.id"],
            name=op.f("fk_loyalty_accounts_customer_id_customers"),
        ),
        sa.PrimaryKeyConstraint("customer_id", name=op.f("pk_loyalty_accounts")),
    )
    op.create_table(
        "points_entries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(length=10), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "kind IN ('earn', 'redeem', 'expire')",
            name=op.f("ck_points_entries_kind_is_known"),
        ),
        sa.CheckConstraint(
            "(kind = 'earn') = (points > 0)",
            name=op.f("ck_points_entries_sign_matches_kind"),
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["loyalty_accounts.customer_id"],
            name=op.f("fk_points_entries_customer_id_loyalty_accounts"),
        ),
        sa.ForeignKeyConstraint(
            ["order_id"], ["orders.id"], name=op.f("fk_points_entries_order_id_orders")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_points_entries")),
    )
    op.create_index(
        "ix_points_entries_customer_created",
        "points_entries",
        ["customer_id", "created_at"],
    )
    op.create_index(
        "uq_points_entries_earn_order",
        "points_entries",
        ["order_id"],
        unique=True,
        postgresql_where=sa.text("kind = 'earn'"),
    )


def downgrade() -> None:
    op.drop_table("points_entries")
    op.drop_table("loyalty_accounts")
    op.drop_table("orders")
    op.drop_table("customers")
