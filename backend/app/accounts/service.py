from app.accounts.models import Account
from app.accounts.repository import AccountRepository
from app.errors import ErrorCode, NotFoundError


class AccountService:
    def __init__(self, accounts: AccountRepository) -> None:
        self._accounts = accounts

    def list_accounts(self) -> list[Account]:
        return self._accounts.find_all()

    def get_account(self, account_id: int) -> Account:
        account = self._accounts.find_by_id(account_id)
        if account is None:
            raise NotFoundError(ErrorCode.ACCOUNT_NOT_FOUND, "Nie znaleziono konta")
        return account

    def find_by_phone_number(self, phone_number: str) -> Account | None:
        return self._accounts.find_by_phone_number(phone_number)
