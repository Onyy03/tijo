from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from app.accounts.models import Account
from app.accounts.service import AccountService
from app.amounts.rules import create_amount_validator
from app.codes.models import BlikCode, BlikCodeStatus
from app.errors import BusinessError, ErrorCode, NotFoundError
from app.history.models import HistoryEntry, HistoryEntryType
from app.payments.models import Payment, PaymentStatus
from app.payments.service import PaymentService
from tests.fakes import (
    FixedClock,
    InMemoryAccountRepository,
    InMemoryBlikCodeRepository,
    InMemoryHistoryRepository,
    InMemoryPaymentRepository,
)

NOW = datetime(2026, 11, 2, 12, 0, 0)
ACCOUNT_ID = 1


@pytest.fixture
def account() -> Account:
    return Account(
        id=ACCOUNT_ID, owner_name="Jan Kowalski", phone_number="500100200", balance_cents=50_000
    )


@pytest.fixture
def codes() -> InMemoryBlikCodeRepository:
    return InMemoryBlikCodeRepository()


@pytest.fixture
def payments() -> InMemoryPaymentRepository:
    return InMemoryPaymentRepository()


@pytest.fixture
def history() -> InMemoryHistoryRepository:
    return InMemoryHistoryRepository()


@pytest.fixture
def service(account, codes, payments, history) -> PaymentService:
    return PaymentService(
        AccountService(InMemoryAccountRepository(account)),
        codes,
        payments,
        history,
        create_amount_validator(),
        FixedClock(NOW),
    )


def start_payment(service: PaymentService, codes: InMemoryBlikCodeRepository) -> Payment:
    codes.add(BlikCode.issue(account_id=ACCOUNT_ID, code="123456", now=NOW))
    return service.create_payment("123456", Decimal("25.00"), "Żabka")


def test_should_create_pending_payment_and_mark_code_as_used_when_code_is_active(
    service, codes, payments
):
    # given
    blik_code = BlikCode.issue(account_id=ACCOUNT_ID, code="123456", now=NOW)
    codes.add(blik_code)

    # when
    payment = service.create_payment("123456", Decimal("25.00"), "Żabka")

    # then
    assert payment.status == PaymentStatus.PENDING
    assert payment.account_id == ACCOUNT_ID
    assert payment.amount_cents == 2500
    assert payment in payments.payments
    assert blik_code.status == BlikCodeStatus.USED


def test_should_reject_payment_when_code_does_not_exist(service):
    # given
    unknown_code = "999999"

    # when
    with pytest.raises(NotFoundError) as error:
        service.create_payment(unknown_code, Decimal("25.00"), "Żabka")

    # then
    assert error.value.code == ErrorCode.CODE_NOT_FOUND


def test_should_reject_payment_when_code_has_expired(service, codes):
    # given
    issued_at = NOW - timedelta(seconds=121)
    codes.add(BlikCode.issue(account_id=ACCOUNT_ID, code="123456", now=issued_at))

    # when
    with pytest.raises(BusinessError) as error:
        service.create_payment("123456", Decimal("25.00"), "Żabka")

    # then
    assert error.value.code == ErrorCode.CODE_EXPIRED


def test_should_reject_payment_when_code_was_already_used(service, codes):
    # given
    codes.add(BlikCode.issue(account_id=ACCOUNT_ID, code="123456", now=NOW))
    service.create_payment("123456", Decimal("25.00"), "Żabka")

    # when
    with pytest.raises(BusinessError) as error:
        service.create_payment("123456", Decimal("10.00"), "Biedronka")

    # then
    assert error.value.code == ErrorCode.CODE_NOT_ACTIVE


def test_should_keep_code_active_when_amount_is_invalid(service, codes):
    # given
    blik_code = BlikCode.issue(account_id=ACCOUNT_ID, code="123456", now=NOW)
    codes.add(blik_code)

    # when
    with pytest.raises(BusinessError):
        service.create_payment("123456", Decimal("0"), "Żabka")

    # then
    assert blik_code.status == BlikCodeStatus.ACTIVE


def test_should_withdraw_funds_and_record_history_when_payment_is_confirmed(
    service, codes, account, history
):
    # given
    payment = start_payment(service, codes)

    # when
    service.confirm(payment.id)

    # then
    assert payment.status == PaymentStatus.CONFIRMED
    assert account.balance_cents == 47_500
    [entry] = history.entries
    assert entry.account_id == ACCOUNT_ID
    assert entry.type == HistoryEntryType.PAYMENT
    assert entry.amount_cents == -2500
    assert entry.description == "Żabka"


def test_should_keep_balance_and_pending_status_when_funds_are_insufficient(
    service, codes, account, history
):
    # given
    account.balance_cents = 1000
    payment = start_payment(service, codes)

    # when
    with pytest.raises(BusinessError) as error:
        service.confirm(payment.id)

    # then
    assert error.value.code == ErrorCode.INSUFFICIENT_FUNDS
    assert account.balance_cents == 1000
    assert payment.status == PaymentStatus.PENDING
    assert history.entries == []


def test_should_reject_confirmation_when_payment_has_expired(service, payments, account):
    # given
    blik_code = BlikCode.issue(account_id=ACCOUNT_ID, code="123456", now=NOW)
    payment = Payment.start(blik_code, "Żabka", 2500, now=NOW - timedelta(seconds=121))
    payments.add(payment)

    # when
    with pytest.raises(BusinessError) as error:
        service.confirm(payment.id)

    # then
    assert error.value.code == ErrorCode.PAYMENT_EXPIRED
    assert account.balance_cents == 50_000


def test_should_mark_payment_as_rejected_without_charging_account(service, codes, account):
    # given
    payment = start_payment(service, codes)

    # when
    service.reject(payment.id)

    # then
    assert payment.status == PaymentStatus.REJECTED
    assert account.balance_cents == 50_000


@pytest.mark.parametrize("decision", ["confirm", "reject"])
def test_should_reject_decision_when_payment_is_not_pending(service, codes, decision):
    # given
    payment = start_payment(service, codes)
    service.reject(payment.id)

    # when
    with pytest.raises(BusinessError) as error:
        getattr(service, decision)(payment.id)

    # then
    assert error.value.code == ErrorCode.PAYMENT_NOT_PENDING


def test_should_raise_not_found_when_confirming_unknown_payment(service):
    # given
    unknown_payment_id = 999

    # when
    with pytest.raises(NotFoundError) as error:
        service.confirm(unknown_payment_id)

    # then
    assert error.value.code == ErrorCode.PAYMENT_NOT_FOUND


def test_should_reject_confirmation_when_daily_spending_limit_would_be_exceeded(
    service, codes, account, history
):
    # given
    account.balance_cents = 300_000
    history.add(
        HistoryEntry(
            account_id=ACCOUNT_ID,
            type=HistoryEntryType.PAYMENT,
            amount_cents=-99_000,
            description="Wcześniejsze zakupy",
            created_at=NOW,
        )
    )
    payment = start_payment(service, codes)

    # when
    with pytest.raises(BusinessError) as error:
        service.confirm(payment.id)

    # then
    assert error.value.code == ErrorCode.DAILY_LIMIT_EXCEEDED
    assert account.balance_cents == 300_000
    assert payment.status == PaymentStatus.PENDING
