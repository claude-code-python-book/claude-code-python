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
