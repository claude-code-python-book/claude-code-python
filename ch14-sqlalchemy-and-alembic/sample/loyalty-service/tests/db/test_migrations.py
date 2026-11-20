from .conftest import alembic


def test_models_and_migrations_agree() -> None:
    result = alembic("check")
    assert "No new upgrade operations detected" in result.stdout + result.stderr


def test_every_migration_can_be_undone_and_redone() -> None:
    alembic("downgrade", "base")
    alembic("upgrade", "head")


def test_there_is_one_head() -> None:
    heads = alembic("heads").stdout.split()
    assert heads.count("(head)") == 1
