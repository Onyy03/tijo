class InvalidPhoneNumberError(ValueError):
    def __init__(self) -> None:
        super().__init__("Numer telefonu musi mieć 9 cyfr")


def normalize_phone_number(raw_number: str) -> str:
    digits = raw_number.replace(" ", "").replace("-", "")
    if digits.startswith("+48"):
        digits = digits[3:]
    elif digits.startswith("0048"):
        digits = digits[4:]
    if len(digits) != 9 or not digits.isdigit():
        raise InvalidPhoneNumberError()
    return digits
