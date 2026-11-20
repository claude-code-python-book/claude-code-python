"""Add reviews and the books rating aggregate.

Revision ID: 0002_reviews
Revises: 0001_books
"""

import sqlalchemy as sa
from alembic import op

revision = "0002_reviews"
down_revision = "0001_books"


def upgrade() -> None:
    op.add_column("books", sa.Column("rating_count", sa.Integer(),
                                     nullable=False, server_default="0"))
    op.add_column("books", sa.Column("rating_total", sa.Integer(),
                                     nullable=False, server_default="0"))
    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("book_id", sa.Integer(),
                  sa.ForeignKey("books.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.String(64), nullable=False),
        sa.Column("stars", sa.Integer(), nullable=False),
        sa.Column("comment", sa.String(2000), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=False,
                  server_default=sa.func.now()),
        sa.UniqueConstraint("book_id", "user_id", name="uq_reviews_book_user"),
        sa.CheckConstraint("stars BETWEEN 1 AND 5", name="ck_reviews_stars"),
    )


def downgrade() -> None:
    op.drop_table("reviews")
    op.drop_column("books", "rating_total")
    op.drop_column("books", "rating_count")
