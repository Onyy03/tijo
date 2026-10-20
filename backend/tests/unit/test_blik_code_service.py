from datetime import datetime, timedelta

from app.accounts.models import Account
from app.accounts.service import AccountService
from app.codes.models import BlikCode, BlikCodeStatus
from app.codes.service import BlikCodeService
from tests.fakes import (
    FixedClock,
    InMemoryAccountRepository,
    InMemoryBlikCodeRepository,
    SequenceCodeGenerator,
)

NOW = datetime(2026, 11, 2, 12, 0, 0)
ACCOUNT_ID = 1
OTHER_ACCOUNT_ID = 2


def create_service(codes: InMemoryBlikCodeRepository, *generated_codes: str) -> BlikCodeService:
    accounts = InMemoryAccountRepository(
        Account(id=ACCOUNT_ID, owner_name="Jan Kowalski", phone_number="500100200", balance_cents=0)
    )
    return BlikCodeService(
        AccountService(accounts), codes, SequenceCodeGenerator(*generated_codes), FixedClock(NOW)
    )


def test_should_set_expiry_to_120_seconds_after_generation():
    # given
    codes = InMemoryBlikCodeRepository()
    service = create_service(codes, "123456")

    # when
    blik_code = service.generate_code(ACCOUNT_ID)

    # then
    assert blik_code.code == "123456"
    assert blik_code.expires_at == NOW + timedelta(seconds=120)
    assert blik_code in codes.codes


def test_should_cancel_previous_active_code_when_generating_new_one():
    # given
    previous = BlikCode.issue(account_id=ACCOUNT_ID, code="111111", now=NOW)
    service = create_service(InMemoryBlikCodeRepository(previous), "222222")

    # when
    service.generate_code(ACCOUNT_ID)

    # then
    assert previous.status == BlikCodeStatus.CANCELLED


def test_should_draw_again_when_generated_code_is_already_in_use():
    # given
    taken = BlikCode.issue(account_id=OTHER_ACCOUNT_ID, code="111111", now=NOW)
    service = create_service(InMemoryBlikCodeRepository(taken), "111111", "222222")

    # when
    blik_code = service.generate_code(ACCOUNT_ID)

    # then
    assert blik_code.code == "222222"
    assert taken.status == BlikCodeStatus.ACTIVE
