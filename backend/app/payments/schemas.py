from marshmallow import Schema, fields, validate

from app.codes.generator import CODE_LENGTH
from app.fields import Money, UtcDateTime
from app.payments.models import PaymentStatus


class CreatePaymentSchema(Schema):
    code = fields.Str(
        required=True,
        validate=validate.Regexp(rf"^\d{{{CODE_LENGTH}}}$", error="Kod BLIK musi mieć 6 cyfr"),
        metadata={"example": "482913"},
    )
    amount = fields.Decimal(required=True, metadata={"example": "25.00"})
    merchant_name = fields.Str(
        required=True, validate=validate.Length(min=1, max=50), metadata={"example": "Żabka"}
    )


class PaymentSchema(Schema):
    id = fields.Int(metadata={"example": 1})
    merchant_name = fields.Str(metadata={"example": "Żabka"})
    amount = Money(attribute="amount_cents", metadata={"example": "25.00"})
    status = fields.Enum(PaymentStatus)
    created_at = UtcDateTime(metadata={"example": "2026-11-02T12:00:00+00:00"})
    expires_at = UtcDateTime(metadata={"example": "2026-11-02T12:02:00+00:00"})
