import pytest

from app.transfers.phone_number import InvalidPhoneNumberError, normalize_phone_number


@pytest.mark.parametrize(
    "raw_number",
    [
        "600200300",
        "600 200 300",
        "600-200-300",
        "+48 600 200 300",
        "+48600200300",
        "0048600200300",
    ],
)
def test_should_return_nine_digits_when_number_is_written_in_common_format(raw_number):
    # given
    # a phone number typed the way people usually write it

    # when
    normalized = normalize_phone_number(raw_number)

    # then
    assert normalized == "600200300"


@pytest.mark.parametrize("raw_number", ["60020030", "6002003001", "60020030a", "+49600200300", ""])
def test_should_reject_number_when_it_is_not_a_nine_digit_polish_number(raw_number):
    # given
    # a value that cannot be turned into a 9-digit Polish phone number

    # when
    with pytest.raises(InvalidPhoneNumberError) as error:
        normalize_phone_number(raw_number)

    # then
    assert str(error.value) == "Numer telefonu musi mieć 9 cyfr"
