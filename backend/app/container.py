from dataclasses import dataclass

from flask import Flask, current_app

from app.accounts.repository import AccountRepository
from app.accounts.service import AccountService

EXTENSION_KEY = "miniblik"


@dataclass(frozen=True)
class Services:
    accounts: AccountService


def init_services(app: Flask) -> None:
    app.extensions[EXTENSION_KEY] = Services(accounts=AccountService(AccountRepository()))


def get_services() -> Services:
    return current_app.extensions[EXTENSION_KEY]
