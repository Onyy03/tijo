from datetime import UTC
from decimal import Decimal

from marshmallow import ValidationError, fields

from app.money import CENTS_PER_UNIT
from app.transfers.phone_number import InvalidPhoneNumberError, normalize_phone_number


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


class PhoneNumber(fields.String):
    """Accepts "600 200 300", "600-200-300" or "+48 600200300" and loads it as "600200300"."""

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return normalize_phone_number(super()._deserialize(value, attr, data, **kwargs))
        except InvalidPhoneNumberError as error:
            raise ValidationError(str(error)) from error
