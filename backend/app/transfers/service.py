from decimal import Decimal

from app.accounts.models import Account
from app.accounts.service import AccountService
from app.amounts.rules import AmountValidator
from app.clock import Clock
from app.errors import BusinessError, ErrorCode, NotFoundError
from app.history.models import HistoryEntry, HistoryEntryType
from app.history.repository import HistoryRepository
from app.money import to_cents


class TransferService:
    def __init__(
        self,
        accounts: AccountService,
        history: HistoryRepository,
        amount_validator: AmountValidator,
        clock: Clock,
    ) -> None:
        self._accounts = accounts
        self._history = history
        self._amount_validator = amount_validator
        self._clock = clock

    def transfer(
        self, from_account_id: int, to_phone_number: str, amount: Decimal, title: str
    ) -> HistoryEntry:
        """Moves money to the account with the given phone number; returns the sender's entry."""
        self._amount_validator.validate(amount)
        sender = self._accounts.get_account(from_account_id)
        recipient = self._find_recipient(sender, to_phone_number)
        amount_cents = to_cents(amount)
        sender.withdraw(amount_cents)
        recipient.deposit(amount_cents)
        return self._record_in_history(sender, recipient, amount_cents, title)

    def _find_recipient(self, sender: Account, phone_number: str) -> Account:
        if sender.phone_number == phone_number:
            raise BusinessError(
                ErrorCode.SELF_TRANSFER, "Nie można wysłać przelewu na własny numer telefonu"
            )
        recipient = self._accounts.find_by_phone_number(phone_number)
        if recipient is None:
            raise NotFoundError(
                ErrorCode.RECIPIENT_NOT_FOUND, "Nie znaleziono odbiorcy o tym numerze telefonu"
            )
        return recipient

    def _record_in_history(
        self, sender: Account, recipient: Account, amount_cents: int, title: str
    ) -> HistoryEntry:
        now = self._clock.now()
        outgoing = HistoryEntry(
            account_id=sender.id,
            type=HistoryEntryType.TRANSFER_OUT,
            amount_cents=-amount_cents,
            description=f"{title} (do: {recipient.owner_name})",
            created_at=now,
        )
        incoming = HistoryEntry(
            account_id=recipient.id,
            type=HistoryEntryType.TRANSFER_IN,
            amount_cents=amount_cents,
            description=f"{title} (od: {sender.owner_name})",
            created_at=now,
        )
        self._history.add(outgoing)
        self._history.add(incoming)
        return outgoing
