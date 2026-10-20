from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from app.amounts.rules import create_amount_validator
from app.codes.models import BlikCode, BlikCodeStatus
from app.errors import BusinessError, ErrorCode, NotFoundError
from app.payments.models import PaymentStatus
from app.payments.service import PaymentService
from tests.fakes import FixedClock, InMemoryBlikCodeRepository, InMemoryPaymentRepository

NOW = datetime(2026, 11, 2, 12, 0, 0)
ACCOUNT_ID = 1


@pytest.fixture
def codes() -> InMemoryBlikCodeRepository:
    return InMemoryBlikCodeRepository()


@pytest.fixture
def payments() -> InMemoryPaymentRepository:
    return InMemoryPaymentRepository()


@pytest.fixture
def service(codes, payments) -> PaymentService:
    return PaymentService(codes, payments, create_amount_validator(), FixedClock(NOW))


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
