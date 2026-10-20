from sqlalchemy import select

from app.accounts.models import Account
from app.extensions import db


class AccountRepository:
    def find_all(self) -> list[Account]:
        return list(db.session.scalars(select(Account).order_by(Account.id)))

    def find_by_id(self, account_id: int) -> Account | None:
        return db.session.get(Account, account_id)
