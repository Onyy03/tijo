from marshmallow import Schema, fields

from app.money import Money


class AccountSchema(Schema):
    id = fields.Int(metadata={"example": 1})
    owner_name = fields.Str(metadata={"example": "Jan Kowalski"})
    phone_number = fields.Str(metadata={"example": "500100200"})
    balance = Money(attribute="balance_cents", metadata={"example": "500.00"})
