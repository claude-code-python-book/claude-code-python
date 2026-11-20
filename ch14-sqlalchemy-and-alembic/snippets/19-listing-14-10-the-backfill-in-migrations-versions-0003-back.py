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
