from datetime import datetime, timedelta

from app.codes.models import BlikCode

ISSUED_AT = datetime(2026, 11, 2, 12, 0, 0)


def test_should_be_active_before_lifetime_passes():
    # given
    blik_code = BlikCode.issue(account_id=1, code="123456", now=ISSUED_AT)

    # when
    is_active = blik_code.is_active_at(ISSUED_AT + timedelta(seconds=119))

    # then
    assert is_active


def test_should_be_inactive_after_lifetime_passes():
    # given
    blik_code = BlikCode.issue(account_id=1, code="123456", now=ISSUED_AT)

    # when
    is_active = blik_code.is_active_at(ISSUED_AT + timedelta(seconds=120))

    # then
    assert not is_active


def test_should_be_inactive_when_cancelled():
    # given
    blik_code = BlikCode.issue(account_id=1, code="123456", now=ISSUED_AT)

    # when
    blik_code.cancel()

    # then
    assert not blik_code.is_active_at(ISSUED_AT)
