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
