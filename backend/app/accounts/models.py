from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.errors import BusinessError, ErrorCode
from app.extensions import db


class Account(db.Model):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_name: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(9), unique=True)
    balance_cents: Mapped[int]

    def withdraw(self, amount_cents: int) -> None:
        if amount_cents > self.balance_cents:
            raise BusinessError(ErrorCode.INSUFFICIENT_FUNDS, "Niewystarczające środki na koncie")
        self.balance_cents -= amount_cents
