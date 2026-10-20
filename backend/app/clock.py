from datetime import UTC, datetime
from typing import Protocol


class Clock(Protocol):
    def now(self) -> datetime: ...


class SystemClock:
    """Current UTC time without timezone info, the format stored in the database."""

    def now(self) -> datetime:
        return datetime.now(UTC).replace(tzinfo=None)
