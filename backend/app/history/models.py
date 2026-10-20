from datetime import datetime
from enum import StrEnum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class HistoryEntryType(StrEnum):
    PAYMENT = "PAYMENT"


class HistoryEntry(db.Model):
    """One change of an account balance. Negative amounts are money leaving the account."""

    __tablename__ = "history_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    type: Mapped[HistoryEntryType]
    amount_cents: Mapped[int]
    description: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime]
