from sqlalchemy import select

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
