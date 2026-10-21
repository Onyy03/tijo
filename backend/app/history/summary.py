from collections.abc import Iterable
from dataclasses import dataclass
from typing import Self

from app.history.models import HistoryEntry


@dataclass(frozen=True)
class AccountSummary:
    incoming_cents: int
    outgoing_cents: int
    operations_count: int

    @classmethod
    def from_entries(cls, entries: Iterable[HistoryEntry]) -> Self:
        amounts = [entry.amount_cents for entry in entries]
        return cls(
            incoming_cents=sum(amount for amount in amounts if amount > 0),
            outgoing_cents=-sum(amount for amount in amounts if amount < 0),
            operations_count=len(amounts),
        )
