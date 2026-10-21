from datetime import datetime

from sqlalchemy import func, select

from app.extensions import db
from app.history.models import HistoryEntry


class HistoryRepository:
    def add(self, entry: HistoryEntry) -> None:
        db.session.add(entry)

    def find_by_account(self, account_id: int) -> list[HistoryEntry]:
        query = (
            select(HistoryEntry)
            .where(HistoryEntry.account_id == account_id)
            .order_by(HistoryEntry.created_at.desc(), HistoryEntry.id.desc())
        )
        return list(db.session.scalars(query))

    def sum_spent_between(self, account_id: int, start: datetime, end: datetime) -> int:
        """Money that left the account in [start, end), as a positive number of cents."""
        query = select(func.coalesce(func.sum(HistoryEntry.amount_cents), 0)).where(
            HistoryEntry.account_id == account_id,
            HistoryEntry.amount_cents < 0,
            HistoryEntry.created_at >= start,
            HistoryEntry.created_at < end,
        )
        return -db.session.scalar(query)
