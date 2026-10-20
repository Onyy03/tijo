from datetime import datetime, timedelta
from enum import StrEnum
from typing import Self

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.codes.generator import CODE_LENGTH
from app.errors import BusinessError, ErrorCode
from app.extensions import db

CODE_LIFETIME = timedelta(seconds=120)


class BlikCodeStatus(StrEnum):
    ACTIVE = "ACTIVE"
    USED = "USED"
    CANCELLED = "CANCELLED"


class BlikCode(db.Model):
    __tablename__ = "blik_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(CODE_LENGTH), index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    created_at: Mapped[datetime]
    expires_at: Mapped[datetime]
    status: Mapped[BlikCodeStatus]

    @classmethod
    def issue(cls, account_id: int, code: str, now: datetime) -> Self:
        return cls(
            account_id=account_id,
            code=code,
            created_at=now,
            expires_at=now + CODE_LIFETIME,
            status=BlikCodeStatus.ACTIVE,
        )

    def is_active_at(self, now: datetime) -> bool:
        return self.status == BlikCodeStatus.ACTIVE and now < self.expires_at

    def cancel(self) -> None:
        self.status = BlikCodeStatus.CANCELLED

    def use(self, now: datetime) -> None:
        if self.status != BlikCodeStatus.ACTIVE:
            raise BusinessError(
                ErrorCode.CODE_NOT_ACTIVE, "Kod BLIK został już wykorzystany lub anulowany"
            )
        if now >= self.expires_at:
            raise BusinessError(ErrorCode.CODE_EXPIRED, "Kod BLIK wygasł")
        self.status = BlikCodeStatus.USED
