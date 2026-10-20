from flask_smorest import Blueprint

from app.codes.models import BlikCode
from app.codes.schemas import BlikCodeSchema
from app.container import get_services
from app.errors import ApiErrorSchema
from app.extensions import db

codes_blueprint = Blueprint(
    "blik_codes", __name__, url_prefix="/api/accounts", description="Kody BLIK"
)


@codes_blueprint.post("/<int:account_id>/blik-codes")
@codes_blueprint.response(201, BlikCodeSchema)
@codes_blueprint.alt_response(404, schema=ApiErrorSchema, description="Nie znaleziono konta")
def generate_blik_code(account_id: int) -> BlikCode:
    """Wygenerowanie kodu BLIK ważnego 120 sekund (poprzedni aktywny kod zostaje anulowany)"""
    blik_code = get_services().codes.generate_code(account_id)
    db.session.commit()
    return blik_code
