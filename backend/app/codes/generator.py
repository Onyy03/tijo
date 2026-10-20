import secrets
from typing import Protocol

CODE_LENGTH = 6


class CodeGenerator(Protocol):
    def generate(self) -> str: ...


class SecureRandomCodeGenerator:
    """Draws BLIK codes from a cryptographically secure random source."""

    def generate(self) -> str:
        return f"{secrets.randbelow(10**CODE_LENGTH):0{CODE_LENGTH}d}"
