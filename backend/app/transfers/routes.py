from flask_smorest import Blueprint

from app.container import get_services
from app.errors import ApiErrorSchema
from app.extensions import db
from app.history.models import HistoryEntry
from app.history.schemas import HistoryEntrySchema
from app.transfers.schemas import CreateTransferSchema

transfers_blueprint = Blueprint(
    "transfers", __name__, url_prefix="/api/transfers", description="Przelewy BLIK na telefon"
)


@transfers_blueprint.post("")
@transfers_blueprint.arguments(CreateTransferSchema, error_status_code=400)
@transfers_blueprint.response(201, HistoryEntrySchema)
@transfers_blueprint.alt_response(
    404, schema=ApiErrorSchema, description="Nie znaleziono konta nadawcy lub odbiorcy"
)
@transfers_blueprint.alt_response(
    422, schema=ApiErrorSchema, description="Brak środków, przelew na własny numer, zła kwota"
)
def create_transfer(data: dict) -> HistoryEntry:
    """Przelew na numer telefonu (zwraca wpis z historii nadawcy)"""
    outgoing = get_services().transfers.transfer(
        data["from_account_id"], data["to_phone_number"], data["amount"], data["title"]
    )
    db.session.commit()
    return outgoing
