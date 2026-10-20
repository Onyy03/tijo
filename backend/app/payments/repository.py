from datetime import datetime

from sqlalchemy import select

from app.extensions import db
from app.payments.models import Payment, PaymentStatus


class PaymentRepository:
    def add(self, payment: Payment) -> None:
        db.session.add(payment)

    def find_by_id(self, payment_id: int) -> Payment | None:
        return db.session.get(Payment, payment_id)

    def find_pending_by_account(self, account_id: int, now: datetime) -> list[Payment]:
        query = (
            select(Payment)
            .where(
                Payment.account_id == account_id,
                Payment.status == PaymentStatus.PENDING,
                Payment.expires_at > now,
            )
            .order_by(Payment.created_at)
        )
        return list(db.session.scalars(query))
