from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from app.accounts.models import Account
from app.codes.models import BlikCode, BlikCodeStatus
from app.payments.models import Payment

if TYPE_CHECKING:
    from app.history.models import HistoryEntry


class FixedClock:
    def __init__(self, now: datetime) -> None:
        self._now = now

    def now(self) -> datetime:
        return self._now


class MutableClock(FixedClock):
    """A clock that tests can move forward, e.g. past the lifetime of a BLIK code."""

    def advance(self, seconds: int) -> None:
        self._now += timedelta(seconds=seconds)


class SequenceCodeGenerator:
    """Returns the given codes one by one, so a test knows which code comes next."""

    def __init__(self, *codes: str) -> None:
        self._codes = iter(codes)

    def generate(self) -> str:
        return next(self._codes)


class InMemoryAccountRepository:
    def __init__(self, *accounts: Account) -> None:
        self._accounts = {account.id: account for account in accounts}

    def find_all(self) -> list[Account]:
        return list(self._accounts.values())

    def find_by_id(self, account_id: int) -> Account | None:
        return self._accounts.get(account_id)

    def find_by_phone_number(self, phone_number: str) -> Account | None:
        return next(
            (
                account
                for account in self._accounts.values()
                if account.phone_number == phone_number
            ),
            None,
        )


class InMemoryBlikCodeRepository:
    def __init__(self, *codes: BlikCode) -> None:
        self.codes = list(codes)

    def add(self, blik_code: BlikCode) -> None:
        self.codes.append(blik_code)

    def find_active_by_account(self, account_id: int) -> list[BlikCode]:
        return [
            blik_code
            for blik_code in self.codes
            if blik_code.account_id == account_id and blik_code.status == BlikCodeStatus.ACTIVE
        ]

    def is_code_in_use(self, code: str, now: datetime) -> bool:
        return any(
            blik_code.code == code and blik_code.is_active_at(now) for blik_code in self.codes
        )

    def find_latest_by_code(self, code: str) -> BlikCode | None:
        return next(
            (blik_code for blik_code in reversed(self.codes) if blik_code.code == code), None
        )


class InMemoryPaymentRepository:
    """Keeps payments in a list and numbers them the way the database would."""

    def __init__(self) -> None:
        self.payments: list[Payment] = []

    def add(self, payment: Payment) -> None:
        payment.id = len(self.payments) + 1
        self.payments.append(payment)

    def find_by_id(self, payment_id: int) -> Payment | None:
        return next((payment for payment in self.payments if payment.id == payment_id), None)


class InMemoryHistoryRepository:
    def __init__(self) -> None:
        self.entries: list[HistoryEntry] = []

    def add(self, entry: "HistoryEntry") -> None:
        self.entries.append(entry)

    def find_by_account(self, account_id: int) -> "list[HistoryEntry]":
        return [entry for entry in self.entries if entry.account_id == account_id]
