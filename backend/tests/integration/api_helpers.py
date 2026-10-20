"""Small wrappers around the MiniBlik API, so integration tests read like a user's steps."""

from flask.testing import FlaskClient
from werkzeug.test import TestResponse

# Demo accounts created by app.seed
JAN_ID = 1
ANNA_ID = 2
PIOTR_ID = 3  # balance 0.00
JAN_PHONE = "500100200"
ANNA_PHONE = "600200300"


def generate_code(client: FlaskClient, account_id: int) -> str:
    response = client.post(f"/api/accounts/{account_id}/blik-codes")
    assert response.status_code == 201
    return response.get_json()["code"]


def start_payment(
    client: FlaskClient, code: str, amount: str = "25.00", merchant_name: str = "Żabka"
) -> TestResponse:
    return client.post(
        "/api/payments", json={"code": code, "amount": amount, "merchant_name": merchant_name}
    )


def create_pending_payment(client: FlaskClient, account_id: int, amount: str = "25.00") -> int:
    response = start_payment(client, generate_code(client, account_id), amount)
    assert response.status_code == 201
    return response.get_json()["id"]


def get_balance(client: FlaskClient, account_id: int) -> str:
    return client.get(f"/api/accounts/{account_id}").get_json()["balance"]


def get_history(client: FlaskClient, account_id: int) -> list[dict]:
    return client.get(f"/api/accounts/{account_id}/history").get_json()
