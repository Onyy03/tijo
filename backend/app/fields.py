from datetime import UTC
from decimal import Decimal

from marshmallow import fields

from app.money import CENTS_PER_UNIT


class Money(fields.String):
    """Amount stored in cents, exposed in the API as a decimal string, e.g. 2500 -> "25.00"."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return f"{Decimal(value) / CENTS_PER_UNIT:.2f}"


class UtcDateTime(fields.DateTime):
    """Serializes naive UTC datetimes from the database with an explicit UTC offset."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return super()._serialize(value.replace(tzinfo=UTC), attr, obj, **kwargs)
