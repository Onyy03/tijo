import pytest

from app.accounts.models import Account
from app.errors import BusinessError, ErrorCode


def create_account(balance_cents: int) -> Account:
    return Account(owner_name="Jan Kowalski", phone_number="500100200", balance_cents=balance_cents)


def test_should_decrease_balance_when_withdrawing_available_funds():
    # given
    account = create_account(balance_cents=5000)

    # when
    account.withdraw(1500)

    # then
    assert account.balance_cents == 3500


def test_should_reject_withdrawal_when_balance_is_insufficient():
    # given
    account = create_account(balance_cents=1000)

    # when
    with pytest.raises(BusinessError) as error:
        account.withdraw(2500)

    # then
    assert error.value.code == ErrorCode.INSUFFICIENT_FUNDS
    assert account.balance_cents == 1000
