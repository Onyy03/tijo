from marshmallow import Schema, fields, validate

from app.codes.generator import CODE_LENGTH
from app.fields import Money, UtcDateTime
from app.payments.models import PaymentStatus

AMOUNT_ERRORS = {
    "required": "Podaj kwotę",
    "invalid": "Kwota musi być liczbą",
    "special": "Kwota musi być liczbą",
}


class CreatePaymentSchema(Schema):
    code = fields.Str(
        required=True,
        validate=validate.Regexp(rf"^\d{{{CODE_LENGTH}}}$", error="Kod BLIK musi mieć 6 cyfr"),
        error_messages={"required": "Podaj kod BLIK"},
        metadata={"example": "482913"},
    )
    amount = fields.Decimal(
        required=True, error_messages=AMOUNT_ERRORS, metadata={"example": "25.00"}
    )
    merchant_name = fields.Str(
        required=True,
        validate=validate.Length(
            min=1, max=50, error="Nazwa sklepu musi mieć od {min} do {max} znaków"
        ),
        error_messages={"required": "Podaj nazwę sklepu"},
        metadata={"example": "Żabka"},
    )


class PaymentSchema(Schema):
    id = fields.Int(metadata={"example": 1})
    merchant_name = fields.Str(metadata={"example": "Żabka"})
    amount = Money(attribute="amount_cents", metadata={"example": "25.00"})
    status = fields.Enum(PaymentStatus)
    created_at = UtcDateTime(metadata={"example": "2026-11-02T12:00:00+00:00"})
    expires_at = UtcDateTime(metadata={"example": "2026-11-02T12:02:00+00:00"})
