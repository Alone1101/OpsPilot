from sqlalchemy import Float, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class OrderDB(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(
        String,
        primary_key = True,
    )

    customer_id: Mapped[str] = mapped_column(
        String,
        nullable = False,
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable = False,
    )

    total_amount: Mapped[float] = mapped_column(
        Float,
        nullable = False,
    )

class RefundDB(Base):
    __tablename__ = "refunds"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        autoincrement = True
    )

    order_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("orders.id"),
        nullable = False
    )

    amount: Mapped[float] = mapped_column(
        Float,
        nullable = False
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable = False
    )