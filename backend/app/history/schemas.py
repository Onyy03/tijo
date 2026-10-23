from marshmallow import Schema, fields

from app.fields import Money, UtcDateTime
from app.history.models import HistoryEntryType


class HistoryEntrySchema(Schema):
    id = fields.Int(metadata={"example": 1})
    type = fields.Enum(HistoryEntryType)
    amount = Money(attribute="amount_cents", metadata={"example": "-25.00"})
    description = fields.Str(metadata={"example": "Żabka"})
    created_at = UtcDateTime(metadata={"example": "2026-11-02T12:00:00+00:00"})


class AccountSummarySchema(Schema):
    total_incoming = Money(attribute="incoming_cents", metadata={"example": "120.50"})
    total_outgoing = Money(attribute="outgoing_cents", metadata={"example": "145.50"})
    operations_count = fields.Int(metadata={"example": 3})
