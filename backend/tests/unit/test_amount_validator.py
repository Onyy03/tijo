from decimal import Decimal

import pytest

from app.amounts.rules import (
    AmountLimitRule,
    AmountScaleRule,
    AmountValidator,
    PositiveAmountRule,
)
from app.errors import BusinessError, ErrorCode

LIMIT = Decimal("5000.00")


def create_validator() -> AmountValidator:
    return AmountValidator([PositiveAmountRule(), AmountScaleRule(), AmountLimitRule(LIMIT)])


@pytest.mark.parametrize("amount", ["0", "0.00", "-5"])
def test_should_reject_amount_when_it_is_not_positive(amount):
    # given
    validator = create_validator()

    # when
    with pytest.raises(BusinessError) as error:
        validator.validate(Decimal(amount))

    # then
    assert error.value.code == ErrorCode.INVALID_AMOUNT


def test_should_reject_amount_when_it_exceeds_limit():
    # given
    validator = create_validator()

    # when
    with pytest.raises(BusinessError) as error:
        validator.validate(Decimal("5000.01"))

    # then
    assert error.value.code == ErrorCode.AMOUNT_LIMIT_EXCEEDED


def test_should_reject_amount_when_it_has_more_than_two_decimal_places():
    # given
    validator = create_validator()

    # when
    with pytest.raises(BusinessError) as error:
        validator.validate(Decimal("10.555"))

    # then
    assert error.value.code == ErrorCode.INVALID_AMOUNT


@pytest.mark.parametrize("amount", ["0.01", "25.50", "1.500", "5000.00"])
def test_should_accept_amount_when_all_rules_pass(amount):
    # given
    validator = create_validator()

    # when
    validator.validate(Decimal(amount))

    # then
    # reaching this line means no rule raised BusinessError
