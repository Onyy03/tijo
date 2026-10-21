from marshmallow import Schema, fields, validate

from app.fields import PhoneNumber

AMOUNT_ERRORS = {
    "required": "Podaj kwotę",
    "invalid": "Kwota musi być liczbą",
    "special": "Kwota musi być liczbą",
}


class CreateTransferSchema(Schema):
    from_account_id = fields.Int(
        required=True,
        error_messages={"required": "Podaj konto nadawcy", "invalid": "Niepoprawne konto"},
        metadata={"example": 1},
    )
    to_phone_number = PhoneNumber(
        required=True,
        error_messages={"required": "Podaj numer telefonu odbiorcy"},
        metadata={"example": "600200300"},
    )
    amount = fields.Decimal(
        required=True, error_messages=AMOUNT_ERRORS, metadata={"example": "120.00"}
    )
    title = fields.Str(
        required=True,
        validate=validate.Length(
            min=1, max=50, error="Tytuł przelewu musi mieć od {min} do {max} znaków"
        ),
        error_messages={"required": "Podaj tytuł przelewu"},
        metadata={"example": "Obiad"},
    )
