from decimal import Decimal

from app.amounts.rules import AmountValidator
from app.clock import Clock
from app.codes.repository import BlikCodeRepository
from app.errors import ErrorCode, NotFoundError
from app.money import to_cents
from app.payments.models import Payment
from app.payments.repository import PaymentRepository


class PaymentService:
    def __init__(
        self,
        codes: BlikCodeRepository,
        payments: PaymentRepository,
        amount_validator: AmountValidator,
        clock: Clock,
    ) -> None:
        self._codes = codes
        self._payments = payments
        self._amount_validator = amount_validator
        self._clock = clock

    def create_payment(self, code: str, amount: Decimal, merchant_name: str) -> Payment:
        self._amount_validator.validate(amount)
        now = self._clock.now()
        blik_code = self._codes.find_latest_by_code(code)
        if blik_code is None:
            raise NotFoundError(ErrorCode.CODE_NOT_FOUND, "Nieprawidłowy kod BLIK")
        blik_code.use(now)
        payment = Payment.start(blik_code, merchant_name, to_cents(amount), now)
        self._payments.add(payment)
        return payment
