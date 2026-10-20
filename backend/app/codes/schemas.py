from datetime import UTC

from marshmallow import Schema, fields


class UtcDateTime(fields.DateTime):
    """Serializes naive UTC datetimes from the database with an explicit UTC offset."""

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return super()._serialize(value.replace(tzinfo=UTC), attr, obj, **kwargs)


class BlikCodeSchema(Schema):
    code = fields.Str(metadata={"example": "482913"})
    expires_at = UtcDateTime(metadata={"example": "2026-11-02T12:02:00+00:00"})
