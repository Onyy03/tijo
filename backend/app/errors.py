from enum import StrEnum

from flask import Flask, Response, jsonify
from marshmallow import Schema, fields


class ErrorCode(StrEnum):
    ACCOUNT_NOT_FOUND = "ACCOUNT_NOT_FOUND"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    INVALID_AMOUNT = "INVALID_AMOUNT"
    AMOUNT_LIMIT_EXCEEDED = "AMOUNT_LIMIT_EXCEEDED"
    CODE_NOT_FOUND = "CODE_NOT_FOUND"
    CODE_NOT_ACTIVE = "CODE_NOT_ACTIVE"
    CODE_EXPIRED = "CODE_EXPIRED"


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


def handle_business_error(error: BusinessError) -> tuple[Response, int]:
    return jsonify(code=error.code, message=error.message), error.http_status


def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(BusinessError, handle_business_error)
