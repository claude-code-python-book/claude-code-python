"""ORM models: customers, orders, and the loyalty ledger."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    MetaData,
    Numeric,
    String,
    func,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Every constraint gets a predictable name, so Alembic can find it again.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Base class for every model."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)
    type_annotation_map = {  # noqa: RUF012 - read by SQLAlchemy, never mutated
        Decimal: Numeric(12, 2),
        datetime: DateTime(timezone=True),
    }


class Customer(Base):
    """Someone who places orders."""

    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    orders: Mapped[list[Order]] = relationship(back_populates="customer", lazy="raise")
    account: Mapped[LoyaltyAccount | None] = relationship(
        back_populates="customer", lazy="raise"
    )

    def __repr__(self) -> str:
        return f"Customer(id={self.id!r}, email={self.email!r})"


class Order(Base):
    """A completed order. Totals are in the shop's single currency."""

    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("total >= 0", name="total_not_negative"),
        Index("ix_orders_customer_placed", "customer_id", "placed_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    total: Mapped[Decimal]
    placed_at: Mapped[datetime] = mapped_column(server_default=func.now())

    customer: Mapped[Customer] = relationship(back_populates="orders", lazy="raise")

    def __repr__(self) -> str:
        return f"Order(id={self.id!r}, total={self.total!r})"


class LoyaltyAccount(Base):
    """One per customer. `balance` is the sum of the ledger, kept in step."""

    __tablename__ = "loyalty_accounts"
    __table_args__ = (
        CheckConstraint("balance >= 0", name="balance_not_negative"),
        CheckConstraint("tier IN ('bronze', 'silver', 'gold')", name="tier_is_known"),
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"), primary_key=True
    )
    balance: Mapped[int] = mapped_column(server_default=text("0"))
    tier: Mapped[str] = mapped_column(String(10), server_default="bronze")
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    customer: Mapped[Customer] = relationship(back_populates="account", lazy="raise")
    entries: Mapped[list[PointsEntry]] = relationship(
        back_populates="account", lazy="raise", order_by="PointsEntry.created_at"
    )


class PointsEntry(Base):
    """One line of the ledger. Lines are only ever added, never changed."""

    __tablename__ = "points_entries"
    __table_args__ = (
        CheckConstraint("kind IN ('earn', 'redeem', 'expire')", name="kind_is_known"),
        CheckConstraint("(kind = 'earn') = (points > 0)", name="sign_matches_kind"),
        # An order earns points once, even if its event is delivered twice.
        Index(
            "uq_points_entries_earn_order",
            "order_id",
            unique=True,
            postgresql_where=text("kind = 'earn'"),
        ),
        Index("ix_points_entries_customer_created", "customer_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("loyalty_accounts.customer_id"))
    kind: Mapped[str] = mapped_column(String(10))
    points: Mapped[int]
    order_id: Mapped[int | None] = mapped_column(ForeignKey("orders.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    account: Mapped[LoyaltyAccount] = relationship(
        back_populates="entries", lazy="raise"
    )
