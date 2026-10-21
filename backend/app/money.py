from decimal import Decimal

CENTS_PER_UNIT = 100
DAILY_SPENDING_LIMIT_CENTS = 100_000


def to_cents(amount: Decimal) -> int:
    return int(amount * CENTS_PER_UNIT)
