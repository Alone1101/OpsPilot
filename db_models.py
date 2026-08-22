from sqlalchemy import Float, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector
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

class EscalationDB(Base):
    __tablename__ = "escalations"

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

    reason: Mapped[str] = mapped_column(
        String,
        nullable = False
    )

    priority: Mapped[str] = mapped_column(
        String,
        nullable = False
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable = False
    )

class PolicyChunkDB(Base):
    __tablename__ = "policy_chunks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        autoincrement = True
    )

    document_name: Mapped[str] = mapped_column(
        String,
        nullable = False
    )

    content: Mapped[str] = mapped_column(
        String,
        nullable = False
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(3072),
        nullable = False
    )