from datetime import datetime
from decimal import Decimal

from app.accounts.service import AccountService
from app.amounts.rules import AmountValidator
from app.clock import Clock
from app.codes.repository import BlikCodeRepository
from app.errors import ErrorCode, NotFoundError
from app.history.models import HistoryEntry, HistoryEntryType
from app.history.repository import HistoryRepository
from app.history.spending_limit import DailySpendingLimit
from app.money import to_cents
from app.payments.models import Payment
from app.payments.repository import PaymentRepository


class PaymentService:
    def __init__(
        self,
        accounts: AccountService,
        codes: BlikCodeRepository,
        payments: PaymentRepository,
        history: HistoryRepository,
        amount_validator: AmountValidator,
        spending_limit: DailySpendingLimit,
        clock: Clock,
    ) -> None:
        self._accounts = accounts
        self._codes = codes
        self._payments = payments
        self._history = history
        self._amount_validator = amount_validator
        self._spending_limit = spending_limit
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

    def get_payment(self, payment_id: int) -> Payment:
        payment = self._payments.find_by_id(payment_id)
        if payment is None:
            raise NotFoundError(ErrorCode.PAYMENT_NOT_FOUND, "Nie znaleziono płatności")
        return payment

    def list_pending(self, account_id: int) -> list[Payment]:
        account = self._accounts.get_account(account_id)
        return self._payments.find_pending_by_account(account.id, self._clock.now())

    def confirm(self, payment_id: int) -> Payment:
        payment = self.get_payment(payment_id)
        account = self._accounts.get_account(payment.account_id)
        now = self._clock.now()
        self._spending_limit.check(account.id, payment.amount_cents, now)
        payment.confirm(account, now)
        self._record_in_history(payment, now)
        return payment

    def reject(self, payment_id: int) -> Payment:
        payment = self.get_payment(payment_id)
        payment.reject()
        return payment

    def cancel(self, payment_id: int) -> Payment:
        payment = self.get_payment(payment_id)
        payment.cancel()
        return payment

    def _record_in_history(self, payment: Payment, now: datetime) -> None:
        self._history.add(
            HistoryEntry(
                account_id=payment.account_id,
                type=HistoryEntryType.PAYMENT,
                amount_cents=-payment.amount_cents,
                description=payment.merchant_name,
                created_at=now,
            )
        )
