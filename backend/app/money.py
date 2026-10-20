from decimal import Decimal

CENTS_PER_UNIT = 100


def to_cents(amount: Decimal) -> int:
    return int(amount * CENTS_PER_UNIT)
