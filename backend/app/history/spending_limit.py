from datetime import datetime, time, timedelta
from decimal import Decimal

from app.errors import BusinessError, ErrorCode
from app.history.repository import HistoryRepository
from app.money import CENTS_PER_UNIT

DAILY_SPENDING_LIMIT_CENTS = 100_000


class DailySpendingLimit:
    """Money leaving an account during one UTC day may not exceed the limit."""

    def __init__(
        self, history: HistoryRepository, limit_cents: int = DAILY_SPENDING_LIMIT_CENTS
    ) -> None:
        self._history = history
        self._limit_cents = limit_cents

    def check(self, account_id: int, amount_cents: int, now: datetime) -> None:
        day_start = datetime.combine(now.date(), time.min)
        day_end = day_start + timedelta(days=1)
        spent_today = self._history.sum_spent_between(account_id, day_start, day_end)
        if spent_today + amount_cents > self._limit_cents:
            limit = Decimal(self._limit_cents) / CENTS_PER_UNIT
            raise BusinessError(
                ErrorCode.DAILY_LIMIT_EXCEEDED,
                f"Przekroczono dzienny limit wydatków {limit:.2f} PLN",
            )
