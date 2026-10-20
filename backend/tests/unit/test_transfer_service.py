from datetime import datetime
from decimal import Decimal

import pytest

from app.accounts.models import Account
from app.accounts.service import AccountService
from app.amounts.rules import create_amount_validator
from app.errors import BusinessError, ErrorCode, NotFoundError
from app.history.models import HistoryEntryType
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
    return TransferService(accounts, history, create_amount_validator(), FixedClock(NOW))


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
