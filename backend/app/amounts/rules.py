from collections.abc import Sequence
from decimal import Decimal
from typing import Protocol

from app.errors import BusinessError, ErrorCode

MAX_AMOUNT = Decimal("5000.00")
SMALLEST_UNIT = Decimal("0.01")


class AmountRule(Protocol):
    def check(self, amount: Decimal) -> None:
        """Raises BusinessError when the amount breaks the rule."""


class PositiveAmountRule:
    def check(self, amount: Decimal) -> None:
        if amount <= 0:
            raise BusinessError(ErrorCode.INVALID_AMOUNT, "Kwota musi być większa od zera")


class AmountScaleRule:
    def check(self, amount: Decimal) -> None:
        if amount != amount.quantize(SMALLEST_UNIT):
            raise BusinessError(
                ErrorCode.INVALID_AMOUNT, "Kwota może mieć najwyżej 2 miejsca po przecinku"
            )


class AmountLimitRule:
    def __init__(self, limit: Decimal) -> None:
        self._limit = limit

    def check(self, amount: Decimal) -> None:
        if amount > self._limit:
            raise BusinessError(
                ErrorCode.AMOUNT_LIMIT_EXCEEDED, f"Kwota przekracza limit {self._limit} PLN"
            )


class AmountValidator:
    def __init__(self, rules: Sequence[AmountRule]) -> None:
        self._rules = rules

    def validate(self, amount: Decimal) -> None:
        for rule in self._rules:
            rule.check(amount)


def create_amount_validator() -> AmountValidator:
    return AmountValidator([PositiveAmountRule(), AmountScaleRule(), AmountLimitRule(MAX_AMOUNT)])
