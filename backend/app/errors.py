from enum import StrEnum


class ErrorCode(StrEnum):
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"


class BusinessError(Exception):
    """Raised when an operation breaks a business rule."""

    def __init__(self, code: ErrorCode, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
