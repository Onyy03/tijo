from sqlalchemy import func, select

from app.accounts.models import Account
from app.extensions import db

DEMO_ACCOUNTS = (
    ("Jan Kowalski", "500100200", 50_000),
    ("Anna Nowak", "600200300", 150_000),
    ("Piotr Zieliński", "700300400", 0),
)


def seed_demo_accounts() -> None:
    """Creates the demo accounts once, when the database has no accounts yet."""
    if db.session.scalar(select(func.count()).select_from(Account)):
        return
    db.session.add_all(
        Account(owner_name=owner_name, phone_number=phone_number, balance_cents=balance_cents)
        for owner_name, phone_number, balance_cents in DEMO_ACCOUNTS
    )
    db.session.commit()
