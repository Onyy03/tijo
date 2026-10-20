import re

from app.codes.generator import SecureRandomCodeGenerator

SIX_DIGITS = re.compile(r"\d{6}")


def test_should_generate_code_made_of_exactly_six_digits():
    # given
    generator = SecureRandomCodeGenerator()

    # when
    codes = [generator.generate() for _ in range(100)]

    # then
    assert all(SIX_DIGITS.fullmatch(code) for code in codes)
