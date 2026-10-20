from datetime import datetime

from sqlalchemy import select

from app.codes.models import BlikCode, BlikCodeStatus
from app.extensions import db


class BlikCodeRepository:
    def add(self, blik_code: BlikCode) -> None:
        db.session.add(blik_code)

    def find_active_by_account(self, account_id: int) -> list[BlikCode]:
        query = select(BlikCode).where(
            BlikCode.account_id == account_id, BlikCode.status == BlikCodeStatus.ACTIVE
        )
        return list(db.session.scalars(query))

    def is_code_in_use(self, code: str, now: datetime) -> bool:
        query = select(BlikCode.id).where(
            BlikCode.code == code,
            BlikCode.status == BlikCodeStatus.ACTIVE,
            BlikCode.expires_at > now,
        )
        return db.session.scalar(query) is not None
