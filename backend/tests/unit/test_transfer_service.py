from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from app.accounts.models import Account
from app.accounts.service import AccountService
from app.amounts.rules import create_amount_validator
from app.errors import BusinessError, ErrorCode, NotFoundError
from app.history.models import HistoryEntry, HistoryEntryType
from app.history.spending_limit import DailySpendingLimit
from app.transfers.service import TransferService
from tests.fakes import FixedClock, InMemoryAccountRepository, InMemoryHistoryRepository

NOW = datetime(2026, 11, 2, 12, 0, 0)
SENDER_ID = 1
RECIPIENT_ID = 2
SENDER_PHONE = "500100200"
RECIPIENT_PHONE = "600200300"


@pytest.fixture
def sender() -> Account:
    return Account(
        id=SENDER_ID, owner_name="Jan Kowalski", phone_number=SENDER_PHONE, balance_cents=50_000
    )


@pytest.fixture
def recipient() -> Account:
    return Account(
        id=RECIPIENT_ID, owner_name="Anna Nowak", phone_number=RECIPIENT_PHONE, balance_cents=10_000
    )


@pytest.fixture
def history() -> InMemoryHistoryRepository:
    return InMemoryHistoryRepository()


@pytest.fixture
def service(sender, recipient, history) -> TransferService:
    accounts = AccountService(InMemoryAccountRepository(sender, recipient))
    return TransferService(
        accounts, history, create_amount_validator(), DailySpendingLimit(history), FixedClock(NOW)
    )


def test_should_move_funds_and_record_both_history_entries_when_transfer_succeeds(
    service, sender, recipient, history
):
    # given
    amount = Decimal("120.00")

    # when
    service.transfer(SENDER_ID, RECIPIENT_PHONE, amount, "Obiad")

    # then
    assert sender.balance_cents == 38_000
    assert recipient.balance_cents == 22_000
    outgoing, incoming = history.entries
    assert (outgoing.account_id, outgoing.type, outgoing.amount_cents) == (
        SENDER_ID,
        HistoryEntryType.TRANSFER_OUT,
        -12_000,
    )
    assert (incoming.account_id, incoming.type, incoming.amount_cents) == (
        RECIPIENT_ID,
        HistoryEntryType.TRANSFER_IN,
        12_000,
    )


def test_should_reject_transfer_when_recipient_is_sender(service, sender):
    # given
    own_phone = SENDER_PHONE

    # when
    with pytest.raises(BusinessError) as error:
        service.transfer(SENDER_ID, own_phone, Decimal("10.00"), "Do siebie")

    # then
    assert error.value.code == ErrorCode.SELF_TRANSFER
    assert sender.balance_cents == 50_000


def test_should_reject_transfer_when_recipient_does_not_exist(service, sender):
    # given
    unknown_phone = "999888777"

    # when
    with pytest.raises(NotFoundError) as error:
        service.transfer(SENDER_ID, unknown_phone, Decimal("10.00"), "Obiad")

    # then
    assert error.value.code == ErrorCode.RECIPIENT_NOT_FOUND
    assert sender.balance_cents == 50_000


def test_should_keep_both_balances_when_sender_has_insufficient_funds(
    service, sender, recipient, history
):
    # given
    amount = Decimal("600.00")

    # when
    with pytest.raises(BusinessError) as error:
        service.transfer(SENDER_ID, RECIPIENT_PHONE, amount, "Za dużo")

    # then
    assert error.value.code == ErrorCode.INSUFFICIENT_FUNDS
    assert sender.balance_cents == 50_000
    assert recipient.balance_cents == 10_000
    assert history.entries == []


def test_should_reject_transfer_when_amount_is_invalid(service):
    # given
    amount = Decimal("-5")

    # when
    with pytest.raises(BusinessError) as error:
        service.transfer(SENDER_ID, RECIPIENT_PHONE, amount, "Ujemna kwota")

    # then
    assert error.value.code == ErrorCode.INVALID_AMOUNT


def history_entry(
    account_id: int, entry_type: HistoryEntryType, amount_cents: int, created_at: datetime
) -> HistoryEntry:
    return HistoryEntry(
        account_id=account_id,
        type=entry_type,
        amount_cents=amount_cents,
        description="Wcześniejsza operacja",
        created_at=created_at,
    )


def test_should_reject_transfer_when_daily_spending_limit_would_be_exceeded(
    service, sender, recipient, history
):
    # given
    sender.balance_cents = 300_000
    history.add(history_entry(SENDER_ID, HistoryEntryType.TRANSFER_OUT, -90_000, NOW))

    # when
    with pytest.raises(BusinessError) as error:
        service.transfer(SENDER_ID, RECIPIENT_PHONE, Decimal("150.00"), "Ponad limit")

    # then
    assert error.value.code == ErrorCode.DAILY_LIMIT_EXCEEDED
    assert sender.balance_cents == 300_000
    assert recipient.balance_cents == 10_000
    assert len(history.entries) == 1


def test_should_allow_transfer_that_reaches_daily_limit_exactly(service, sender, history):
    # given
    sender.balance_cents = 300_000
    history.add(history_entry(SENDER_ID, HistoryEntryType.PAYMENT, -90_000, NOW))

    # when
    service.transfer(SENDER_ID, RECIPIENT_PHONE, Decimal("100.00"), "Równo limit")

    # then
    assert sender.balance_cents == 290_000


def test_should_not_count_spending_from_previous_day_towards_daily_limit(service, sender, history):
    # given
    sender.balance_cents = 300_000
    yesterday = NOW - timedelta(days=1)
    history.add(history_entry(SENDER_ID, HistoryEntryType.TRANSFER_OUT, -90_000, yesterday))

    # when
    service.transfer(SENDER_ID, RECIPIENT_PHONE, Decimal("150.00"), "Nowy dzień")

    # then
    assert sender.balance_cents == 285_000


def test_should_not_count_incoming_money_towards_daily_limit(service, sender, history):
    # given
    history.add(history_entry(SENDER_ID, HistoryEntryType.TRANSFER_IN, 90_000, NOW))

    # when
    service.transfer(SENDER_ID, RECIPIENT_PHONE, Decimal("150.00"), "Po wpływie")

    # then
    assert sender.balance_cents == 35_000
