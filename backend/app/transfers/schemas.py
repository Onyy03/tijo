from marshmallow import Schema, fields, validate


class CreateTransferSchema(Schema):
    from_account_id = fields.Int(required=True, metadata={"example": 1})
    to_phone_number = fields.Str(
        required=True,
        validate=validate.Regexp(r"^\d{9}$", error="Numer telefonu musi mieć 9 cyfr"),
        metadata={"example": "600200300"},
    )
    amount = fields.Decimal(required=True, metadata={"example": "120.00"})
    title = fields.Str(
        required=True, validate=validate.Length(min=1, max=50), metadata={"example": "Obiad"}
    )
