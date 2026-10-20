from enum import StrEnum


class ErrorCode(StrEnum):
    ACCOUNT_NOT_FOUND = "ACCOUNT_NOT_FOUND"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"


class BusinessError(Exception):
    """Raised when an operation breaks a business rule."""

    def __init__(self, code: ErrorCode, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class NotFoundError(BusinessError):
    """Raised when a requested resource does not exist."""
