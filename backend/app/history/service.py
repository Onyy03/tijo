from types import SimpleNamespace

from app.accounts.service import AccountService
from app.history.models import HistoryEntry
from app.history.repository import HistoryRepository


class HistoryService:
    def __init__(self, accounts: AccountService, history: HistoryRepository) -> None:
        self._accounts = accounts
        self._history = history

    def list_for_account(self, account_id: int) -> list[HistoryEntry]:
        account = self._accounts.get_account(account_id)
        return self._history.find_by_account(account.id)

    def summarize(self, account_id: int) -> SimpleNamespace:
        account = self._accounts.get_account(account_id)
        incoming_cents = 0
        outgoing_cents = 0
        operations_count = 0
        for entry in self._history.find_by_account(account.id):
            if entry.amount_cents > 0:
                incoming_cents += entry.amount_cents
            else:
                outgoing_cents += -entry.amount_cents
            operations_count += 1
        return SimpleNamespace(
            incoming_cents=incoming_cents,
            outgoing_cents=outgoing_cents,
            operations_count=operations_count,
        )
