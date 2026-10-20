from marshmallow import Schema, fields

from app.fields import UtcDateTime


class BlikCodeSchema(Schema):
    code = fields.Str(metadata={"example": "482913"})
    expires_at = UtcDateTime(metadata={"example": "2026-11-02T12:02:00+00:00"})
