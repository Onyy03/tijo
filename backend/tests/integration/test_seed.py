from sqlalchemy import func, select

from app.accounts.models import Account
from app.extensions import db
from app.seed import seed_demo_accounts


def test_should_not_duplicate_demo_accounts_when_seeding_again(app):
    # given
    # the application already created the demo accounts on start

    # when
    with app.app_context():
        seed_demo_accounts()
        account_count = db.session.scalar(select(func.count()).select_from(Account))

    # then
    assert account_count == 3
