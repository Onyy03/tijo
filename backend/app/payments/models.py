from datetime import datetime, timedelta
from enum import StrEnum
from typing import Self

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.accounts.models import Account
from app.codes.models import BlikCode
from app.errors import BusinessError, ErrorCode
from app.extensions import db

PAYMENT_LIFETIME = timedelta(seconds=120)


class PaymentStatus(StrEnum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"


class Payment(db.Model):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    blik_code_id: Mapped[int] = mapped_column(ForeignKey("blik_codes.id"))
    merchant_name: Mapped[str] = mapped_column(String(50))
    amount_cents: Mapped[int]
    status: Mapped[PaymentStatus]
    created_at: Mapped[datetime]
    expires_at: Mapped[datetime]

    @classmethod
    def start(
        cls, blik_code: BlikCode, merchant_name: str, amount_cents: int, now: datetime
    ) -> Self:
        return cls(
            account_id=blik_code.account_id,
            blik_code_id=blik_code.id,
            merchant_name=merchant_name,
            amount_cents=amount_cents,
            status=PaymentStatus.PENDING,
            created_at=now,
            expires_at=now + PAYMENT_LIFETIME,
        )

    def confirm(self, account: Account, now: datetime) -> None:
        self._ensure_pending()
        if now >= self.expires_at:
            raise BusinessError(ErrorCode.PAYMENT_EXPIRED, "Czas na potwierdzenie płatności minął")
        account.withdraw(self.amount_cents)
        self.status = PaymentStatus.CONFIRMED

    def reject(self) -> None:
        self._ensure_pending()
        self.status = PaymentStatus.REJECTED

    def _ensure_pending(self) -> None:
        if self.status != PaymentStatus.PENDING:
            raise BusinessError(ErrorCode.PAYMENT_NOT_PENDING, "Płatność została już rozliczona")
