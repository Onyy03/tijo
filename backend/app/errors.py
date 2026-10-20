from enum import StrEnum

from flask import Flask, Response, jsonify
from marshmallow import Schema, fields
from werkzeug.exceptions import BadRequest


class ErrorCode(StrEnum):
    VALIDATION_ERROR = "VALIDATION_ERROR"
    ACCOUNT_NOT_FOUND = "ACCOUNT_NOT_FOUND"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    INVALID_AMOUNT = "INVALID_AMOUNT"
    AMOUNT_LIMIT_EXCEEDED = "AMOUNT_LIMIT_EXCEEDED"
    CODE_NOT_FOUND = "CODE_NOT_FOUND"
    CODE_NOT_ACTIVE = "CODE_NOT_ACTIVE"
    CODE_EXPIRED = "CODE_EXPIRED"
    PAYMENT_NOT_FOUND = "PAYMENT_NOT_FOUND"
    PAYMENT_NOT_PENDING = "PAYMENT_NOT_PENDING"
    PAYMENT_EXPIRED = "PAYMENT_EXPIRED"
    SELF_TRANSFER = "SELF_TRANSFER"
    RECIPIENT_NOT_FOUND = "RECIPIENT_NOT_FOUND"


class BusinessError(Exception):
    """Raised when an operation breaks a business rule."""

    http_status = 422

    def __init__(self, code: ErrorCode, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class NotFoundError(BusinessError):
    """Raised when a requested resource does not exist."""

    http_status = 404


class ApiErrorSchema(Schema):
    code = fields.Str(metadata={"example": ErrorCode.ACCOUNT_NOT_FOUND.value})
    message = fields.Str(metadata={"example": "Nie znaleziono konta"})
    errors = fields.Dict(metadata={"description": "Field errors, only for VALIDATION_ERROR"})


def handle_business_error(error: BusinessError) -> tuple[Response, int]:
    return jsonify(code=error.code, message=error.message), error.http_status


def handle_validation_error(error: BadRequest) -> tuple[Response, int]:
    """Request data rejected by a schema; webargs puts the field errors in `error.data`."""
    field_errors = getattr(error, "data", {}).get("messages", {})
    body = jsonify(
        code=ErrorCode.VALIDATION_ERROR,
        message="Niepoprawne dane wejściowe",
        errors=field_errors,
    )
    return body, 400


def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(BusinessError, handle_business_error)
    app.register_error_handler(BadRequest, handle_validation_error)
