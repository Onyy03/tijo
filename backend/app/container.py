from dataclasses import dataclass

from flask import Flask, current_app

from app.accounts.repository import AccountRepository
from app.accounts.service import AccountService
from app.amounts.rules import create_amount_validator
from app.clock import Clock
from app.codes.generator import CodeGenerator
from app.codes.repository import BlikCodeRepository
from app.codes.service import BlikCodeService
from app.history.repository import HistoryRepository
from app.history.service import HistoryService
from app.history.spending_limit import DailySpendingLimit
from app.payments.repository import PaymentRepository
from app.payments.service import PaymentService
from app.transfers.service import TransferService

EXTENSION_KEY = "miniblik"


@dataclass(frozen=True)
class Services:
    accounts: AccountService
    codes: BlikCodeService
    payments: PaymentService
    transfers: TransferService
    history: HistoryService


def init_services(app: Flask, clock: Clock, code_generator: CodeGenerator) -> None:
    accounts = AccountService(AccountRepository())
    code_repository = BlikCodeRepository()
    history_repository = HistoryRepository()
    amount_validator = create_amount_validator()
    spending_limit = DailySpendingLimit(history_repository)
    app.extensions[EXTENSION_KEY] = Services(
        accounts=accounts,
        codes=BlikCodeService(accounts, code_repository, code_generator, clock),
        payments=PaymentService(
            accounts,
            code_repository,
            PaymentRepository(),
            history_repository,
            amount_validator,
            spending_limit,
            clock,
        ),
        transfers=TransferService(
            accounts, history_repository, amount_validator, spending_limit, clock
        ),
        history=HistoryService(accounts, history_repository),
    )


def get_services() -> Services:
    return current_app.extensions[EXTENSION_KEY]
