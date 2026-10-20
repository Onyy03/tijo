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
from app.payments.repository import PaymentRepository
from app.payments.service import PaymentService

EXTENSION_KEY = "miniblik"


@dataclass(frozen=True)
class Services:
    accounts: AccountService
    codes: BlikCodeService
    payments: PaymentService


def init_services(app: Flask, clock: Clock, code_generator: CodeGenerator) -> None:
    accounts = AccountService(AccountRepository())
    code_repository = BlikCodeRepository()
    codes = BlikCodeService(accounts, code_repository, code_generator, clock)
    payments = PaymentService(
        accounts,
        code_repository,
        PaymentRepository(),
        HistoryRepository(),
        create_amount_validator(),
        clock,
    )
    app.extensions[EXTENSION_KEY] = Services(accounts=accounts, codes=codes, payments=payments)


def get_services() -> Services:
    return current_app.extensions[EXTENSION_KEY]
