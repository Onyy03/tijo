from flask_smorest import Blueprint

from app.accounts.models import Account
from app.accounts.schemas import AccountSchema
from app.container import get_services
from app.errors import ApiErrorSchema

accounts_blueprint = Blueprint(
    "accounts", __name__, url_prefix="/api/accounts", description="Konta użytkowników"
)


@accounts_blueprint.get("")
@accounts_blueprint.response(200, AccountSchema(many=True))
def list_accounts() -> list[Account]:
    """Lista wszystkich kont"""
    return get_services().accounts.list_accounts()


@accounts_blueprint.get("/<int:account_id>")
@accounts_blueprint.response(200, AccountSchema)
@accounts_blueprint.alt_response(404, schema=ApiErrorSchema, description="Nie znaleziono konta")
def get_account(account_id: int) -> Account:
    """Dane i saldo konta"""
    return get_services().accounts.get_account(account_id)
