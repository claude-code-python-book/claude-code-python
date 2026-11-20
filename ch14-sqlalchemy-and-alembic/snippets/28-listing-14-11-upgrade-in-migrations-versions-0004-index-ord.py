def upgrade() -> None:
    with op.get_context().autocommit_block():
        op.create_index(
            "ix_orders_customer_placed",
            "orders",
            ["customer_id", "placed_at"],
            postgresql_concurrently=True,
        )
