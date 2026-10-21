import re

SEPARATORS = re.compile(r"[ -]")
PHONE_NUMBER = re.compile(r"(?:\+48|0048)?(\d{9})")


class InvalidPhoneNumberError(ValueError):
    def __init__(self) -> None:
        super().__init__("Numer telefonu musi mieć 9 cyfr")


def normalize_phone_number(raw_number: str) -> str:
    """Turns "600 200 300", "600-200-300" or "+48 600200300" into "600200300"."""
    match = PHONE_NUMBER.fullmatch(SEPARATORS.sub("", raw_number))
    if match is None:
        raise InvalidPhoneNumberError()
    return match.group(1)
