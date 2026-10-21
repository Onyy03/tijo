from marshmallow import Schema, ValidationError, fields, pre_load, validate

from app.transfers.phone_number import InvalidPhoneNumberError, normalize_phone_number

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
    to_phone_number = fields.Str(
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

    @pre_load
    def normalize_recipient_phone(self, data, **kwargs):
        phone = data.get("to_phone_number") if isinstance(data, dict) else None
        if not isinstance(phone, str):
            return data
        try:
            return {**data, "to_phone_number": normalize_phone_number(phone)}
        except InvalidPhoneNumberError as error:
            raise ValidationError(str(error), field_name="to_phone_number") from error
