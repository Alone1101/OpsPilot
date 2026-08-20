from sqlalchemy import Float, String
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