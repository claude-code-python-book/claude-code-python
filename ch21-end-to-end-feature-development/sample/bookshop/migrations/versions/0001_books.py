"""Create the books table.

Revision ID: 0001_books
Revises:
"""

import sqlalchemy as sa
from alembic import op

revision = "0001_books"
down_revision = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(300), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("books")
