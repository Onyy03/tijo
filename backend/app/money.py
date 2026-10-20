from decimal import Decimal

from marshmallow import fields

CENTS_PER_UNIT = 100


def to_cents(amount: Decimal) -> int:
    return int(amount * CENTS_PER_UNIT)


class Money(fields.String):
    """Amount stored in cents, exposed in the API as a decimal string, e.g. 2500 -> "25.00"."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return f"{Decimal(value) / CENTS_PER_UNIT:.2f}"
