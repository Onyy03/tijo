from app.accounts.service import AccountService
from app.history.models import HistoryEntry
from app.history.repository import HistoryRepository
from app.history.summary import AccountSummary


class HistoryService:
    def __init__(self, accounts: AccountService, history: HistoryRepository) -> None:
        self._accounts = accounts
        self._history = history

    def list_for_account(self, account_id: int) -> list[HistoryEntry]:
        account = self._accounts.get_account(account_id)
        return self._history.find_by_account(account.id)

    def summarize(self, account_id: int) -> AccountSummary:
        account = self._accounts.get_account(account_id)
        return AccountSummary.from_entries(self._history.find_by_account(account.id))
