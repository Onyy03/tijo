from dataclasses import dataclass

from flask import Flask, current_app

from app.accounts.repository import AccountRepository
from app.accounts.service import AccountService
from app.clock import Clock
from app.codes.generator import CodeGenerator
from app.codes.repository import BlikCodeRepository
from app.codes.service import BlikCodeService

EXTENSION_KEY = "miniblik"


@dataclass(frozen=True)
class Services:
    accounts: AccountService
    codes: BlikCodeService


def init_services(app: Flask, clock: Clock, code_generator: CodeGenerator) -> None:
    accounts = AccountService(AccountRepository())
    codes = BlikCodeService(accounts, BlikCodeRepository(), code_generator, clock)
    app.extensions[EXTENSION_KEY] = Services(accounts=accounts, codes=codes)


def get_services() -> Services:
    return current_app.extensions[EXTENSION_KEY]
