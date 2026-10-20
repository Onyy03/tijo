from datetime import datetime

import pytest
from marshmallow import Schema

from app.fields import Money, UtcDateTime


class ExampleSchema(Schema):
    amount = Money(attribute="amount_cents")
    created_at = UtcDateTime()


@pytest.mark.parametrize(
    ("amount_cents", "expected"), [(2500, "25.00"), (-12050, "-120.50"), (0, "0.00")]
)
def test_should_serialize_cents_as_decimal_string(amount_cents, expected):
    # given
    data = {"amount_cents": amount_cents, "created_at": None}

    # when
    result = ExampleSchema().dump(data)

    # then
    assert result["amount"] == expected


def test_should_add_utc_offset_to_datetime_from_database():
    # given
    data = {"amount_cents": 0, "created_at": datetime(2026, 11, 2, 12, 0, 0)}

    # when
    result = ExampleSchema().dump(data)

    # then
    assert result["created_at"] == "2026-11-02T12:00:00+00:00"


def test_should_keep_missing_values_empty():
    # given
    data = {"amount_cents": None, "created_at": None}

    # when
    result = ExampleSchema().dump(data)

    # then
    assert result == {"amount": None, "created_at": None}
