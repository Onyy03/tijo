from app.extensions import db
from app.history.models import HistoryEntry


class HistoryRepository:
    def add(self, entry: HistoryEntry) -> None:
        db.session.add(entry)
