from flask_smorest import Blueprint

from app.container import get_services
from app.errors import ApiErrorSchema
from app.history.models import HistoryEntry
from app.history.schemas import AccountSummarySchema, HistoryEntrySchema

history_blueprint = Blueprint(
    "history", __name__, url_prefix="/api/accounts", description="Historia operacji"
)


@history_blueprint.get("/<int:account_id>/history")
@history_blueprint.response(200, HistoryEntrySchema(many=True))
@history_blueprint.alt_response(404, schema=ApiErrorSchema, description="Nie znaleziono konta")
def list_history(account_id: int) -> list[HistoryEntry]:
    """Historia operacji na koncie, od najnowszej"""
    return get_services().history.list_for_account(account_id)


@history_blueprint.get("/<int:account_id>/summary")
@history_blueprint.response(200, AccountSummarySchema)
@history_blueprint.alt_response(404, schema=ApiErrorSchema, description="Nie znaleziono konta")
def get_summary(account_id: int):
    """Suma wpływów i wydatków na koncie oraz liczba operacji"""
    return get_services().history.summarize(account_id)
