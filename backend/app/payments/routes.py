from flask_smorest import Blueprint

from app.container import get_services
from app.errors import ApiErrorSchema
from app.extensions import db
from app.payments.models import Payment
from app.payments.schemas import CreatePaymentSchema, PaymentSchema

payments_blueprint = Blueprint(
    "payments", __name__, url_prefix="/api", description="Płatności BLIK"
)


@payments_blueprint.post("/payments")
@payments_blueprint.arguments(CreatePaymentSchema, error_status_code=400)
@payments_blueprint.response(201, PaymentSchema)
@payments_blueprint.alt_response(404, schema=ApiErrorSchema, description="Nieprawidłowy kod BLIK")
@payments_blueprint.alt_response(
    422, schema=ApiErrorSchema, description="Kod wygasł lub był już użyty, niepoprawna kwota"
)
def create_payment(data: dict) -> Payment:
    """Rozpoczęcie płatności kodem BLIK w terminalu sklepu"""
    payment = get_services().payments.create_payment(
        data["code"], data["amount"], data["merchant_name"]
    )
    db.session.commit()
    return payment


@payments_blueprint.get("/payments/<int:payment_id>")
@payments_blueprint.response(200, PaymentSchema)
@payments_blueprint.alt_response(404, schema=ApiErrorSchema, description="Nie znaleziono płatności")
def get_payment(payment_id: int) -> Payment:
    """Status płatności (odpytywany przez terminal)"""
    return get_services().payments.get_payment(payment_id)


@payments_blueprint.post("/payments/<int:payment_id>/confirm")
@payments_blueprint.response(200, PaymentSchema)
@payments_blueprint.alt_response(404, schema=ApiErrorSchema, description="Nie znaleziono płatności")
@payments_blueprint.alt_response(
    422, schema=ApiErrorSchema, description="Brak środków, płatność wygasła lub jest rozliczona"
)
def confirm_payment(payment_id: int) -> Payment:
    """Zatwierdzenie płatności w aplikacji bankowej"""
    payment = get_services().payments.confirm(payment_id)
    db.session.commit()
    return payment


@payments_blueprint.post("/payments/<int:payment_id>/reject")
@payments_blueprint.response(200, PaymentSchema)
@payments_blueprint.alt_response(404, schema=ApiErrorSchema, description="Nie znaleziono płatności")
@payments_blueprint.alt_response(
    422, schema=ApiErrorSchema, description="Płatność jest już rozliczona"
)
def reject_payment(payment_id: int) -> Payment:
    """Odrzucenie płatności w aplikacji bankowej"""
    payment = get_services().payments.reject(payment_id)
    db.session.commit()
    return payment


@payments_blueprint.get("/accounts/<int:account_id>/pending-payments")
@payments_blueprint.response(200, PaymentSchema(many=True))
@payments_blueprint.alt_response(404, schema=ApiErrorSchema, description="Nie znaleziono konta")
def list_pending_payments(account_id: int) -> list[Payment]:
    """Płatności czekające na potwierdzenie w aplikacji bankowej"""
    return get_services().payments.list_pending(account_id)
