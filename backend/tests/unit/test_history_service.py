from datetime import datetime

import pytest

from app.accounts.models import Account
from app.accounts.service import AccountService
from app.errors import ErrorCode, NotFoundError
from app.history.models import HistoryEntry, HistoryEntryType
from app.history.service import HistoryService
from tests.fakes import InMemoryAccountRepository, InMemoryHistoryRepository

NOW = datetime(2026, 11, 2, 12, 0, 0)
ACCOUNT_ID = 1
OTHER_ACCOUNT_ID = 2


@pytest.fixture
def history() -> InMemoryHistoryRepository:
    return InMemoryHistoryRepository()


@pytest.fixture
def service(history) -> HistoryService:
    account = Account(
        id=ACCOUNT_ID, owner_name="Jan Kowalski", phone_number="500100200", balance_cents=0
    )
    return HistoryService(AccountService(InMemoryAccountRepository(account)), history)


def history_entry(account_id: int, entry_type: HistoryEntryType, amount_cents: int) -> HistoryEntry:
    return HistoryEntry(
        account_id=account_id,
        type=entry_type,
        amount_cents=amount_cents,
        description="Operacja",
        created_at=NOW,
    )


def test_should_sum_incoming_and_outgoing_money_separately(service, history):
    # given
    history.add(history_entry(ACCOUNT_ID, HistoryEntryType.PAYMENT, -2500))
    history.add(history_entry(ACCOUNT_ID, HistoryEntryType.TRANSFER_OUT, -12050))
    history.add(history_entry(ACCOUNT_ID, HistoryEntryType.TRANSFER_IN, 5000))
    history.add(history_entry(OTHER_ACCOUNT_ID, HistoryEntryType.TRANSFER_IN, 12050))

    # when
    summary = service.summarize(ACCOUNT_ID)

    # then
    assert summary.incoming_cents == 5000
    assert summary.outgoing_cents == 14550
    assert summary.operations_count == 3


def test_should_return_zeros_when_account_has_no_operations(service):
    # given
    # the account exists but has no history entries

    # when
    summary = service.summarize(ACCOUNT_ID)

    # then
    assert (summary.incoming_cents, summary.outgoing_cents, summary.operations_count) == (0, 0, 0)


def test_should_raise_not_found_when_summarizing_unknown_account(service):
    # given
    unknown_account_id = 999

    # when
    with pytest.raises(NotFoundError) as error:
        service.summarize(unknown_account_id)

    # then
    assert error.value.code == ErrorCode.ACCOUNT_NOT_FOUND
