from pathlib import Path
from textwrap import dedent

import pytest

from tools.check_migrations import check_source, main

VERSIONS = Path(__file__).parents[1] / "migrations" / "versions"


def codes(body: str) -> list[str]:
    source = "from alembic import op\nimport sqlalchemy as sa\n\n\n" + dedent(body)
    return [f.code for f in check_source(source)]


def test_the_projects_own_migrations_are_clean() -> None:
    assert main(sorted(str(p) for p in VERSIONS.glob("*.py"))) == 0


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        (  # a plain index on an existing table
            """
            def upgrade():
                op.create_index("ix_orders_total", "orders", ["total"])
            """,
            ["MIG001"],
        ),
        (  # an index on a table created in the same migration is fine
            """
            def upgrade():
                op.create_table("tags", sa.Column("id", sa.Integer()))
                op.create_index("ix_tags_id", "tags", ["id"])
            """,
            [],
        ),
        (  # CONCURRENTLY outside an autocommit block
            """
            def upgrade():
                op.create_index("ix_o", "orders", ["total"],
                                postgresql_concurrently=True)
            """,
            ["MIG002"],
        ),
        (  # ...and inside one
            """
            def upgrade():
                with op.get_context().autocommit_block():
                    op.create_index("ix_o", "orders", ["total"],
                                    postgresql_concurrently=True)
            """,
            [],
        ),
        (
            """
            def upgrade():
                op.add_column("orders", sa.Column("note", sa.Text(), nullable=False))
            """,
            ["MIG003"],
        ),
        (  # NOT NULL with a constant default is safe on PostgreSQL 11+
            """
            def upgrade():
                op.add_column("orders", sa.Column(
                    "channel", sa.String(10), nullable=False, server_default="web"))
            """,
            [],
        ),
        (
            """
            def upgrade():
                op.add_column("orders", sa.Column(
                    "ref", sa.Uuid(), server_default=sa.text("gen_random_uuid()")))
            """,
            ["MIG004"],
        ),
        (  # now() is stable, not volatile: no rewrite
            """
            def upgrade():
                op.add_column("orders", sa.Column(
                    "seen_at", sa.DateTime(), server_default=sa.func.now()))
            """,
            [],
        ),
        (
            """
            def upgrade():
                op.alter_column("orders", "total", type_=sa.Numeric(14, 2))
            """,
            ["MIG005"],
        ),
        (
            """
            def upgrade():
                op.alter_column("loyalty_accounts", "tier", nullable=False)
            """,
            ["MIG006"],
        ),
        (
            """
            def upgrade():
                op.drop_column("customers", "name")
            """,
            ["MIG007"],
        ),
        (  # only upgrade() is checked
            """
            def downgrade():
                op.drop_column("customers", "name")
            """,
            [],
        ),
        (
            """
            from loyalty.rules import tier_for

            def upgrade():
                pass
            """,
            ["MIG008"],
        ),
    ],
)
def test_each_rule(body: str, expected: list[str]) -> None:
    assert codes(body) == expected


def test_a_rename_from_autogenerate_is_caught() -> None:
    body = """
        def upgrade():
            op.add_column("customers", sa.Column("full_name", sa.String(200),
                          nullable=False))
            op.drop_column("customers", "name")
        """
    assert codes(body) == ["MIG003", "MIG007"]


def test_a_finding_can_be_accepted_on_its_line() -> None:
    body = """
        def upgrade():
            op.drop_column("customers", "fax")  # migration-ok: MIG007 unused since v2
        """
    assert codes(body) == []


def test_accepting_one_code_does_not_hide_another() -> None:
    body = """
        def upgrade():
            op.drop_column("customers", "fax")  # migration-ok: MIG001
        """
    assert codes(body) == ["MIG007"]
