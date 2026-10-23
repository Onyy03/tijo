from flask.testing import FlaskClient
from werkzeug.test import TestResponse

from tests.integration.api_helpers import (
    ANNA_ID,
    ANNA_PHONE,
    JAN_ID,
    JAN_PHONE,
    get_balance,
    get_history,
)


def send_transfer(client: FlaskClient, **overrides: object) -> TestResponse:
    body = {
        "from_account_id": JAN_ID,
        "to_phone_number": ANNA_PHONE,
        "amount": "120.00",
        "title": "Obiad",
    }
    return client.post("/api/transfers", json=body | overrides)


def test_should_move_funds_between_accounts_when_transfer_is_valid(client):
    # given
    amount = "120.00"

    # when
    response = send_transfer(client, amount=amount)

    # then
    assert response.status_code == 201
    body = response.get_json()
    assert (body["type"], body["amount"]) == ("TRANSFER_OUT", "-120.00")
    assert get_balance(client, JAN_ID) == "380.00"
    assert get_balance(client, ANNA_ID) == "1620.00"


def test_should_return_not_found_when_recipient_phone_is_unknown(client):
    # given
    unknown_phone = "999888777"

    # when
    response = send_transfer(client, to_phone_number=unknown_phone)

    # then
    assert response.status_code == 404
    assert response.get_json()["code"] == "RECIPIENT_NOT_FOUND"
    assert get_balance(client, JAN_ID) == "500.00"


def test_should_show_transfer_in_history_of_both_accounts(client):
    # given
    send_transfer(client, amount="50.00", title="Kino")

    # when
    sender_history = get_history(client, JAN_ID)
    recipient_history = get_history(client, ANNA_ID)

    # then
    assert [(entry["type"], entry["amount"]) for entry in sender_history] == [
        ("TRANSFER_OUT", "-50.00")
    ]
    assert [(entry["type"], entry["amount"]) for entry in recipient_history] == [
        ("TRANSFER_IN", "50.00")
    ]


def test_should_accept_recipient_phone_written_with_spaces_and_country_prefix(client):
    # given
    phone_with_prefix = "+48 600 200 300"

    # when
    response = send_transfer(client, to_phone_number=phone_with_prefix)

    # then
    assert response.status_code == 201
    assert get_balance(client, ANNA_ID) == "1620.00"


def test_should_reject_transfer_when_daily_spending_limit_is_exceeded(client):
    # given
    first = send_transfer(
        client, from_account_id=ANNA_ID, to_phone_number=JAN_PHONE, amount="600.00"
    )
    assert first.status_code == 201

    # when
    response = send_transfer(
        client, from_account_id=ANNA_ID, to_phone_number=JAN_PHONE, amount="500.00"
    )

    # then
    assert response.status_code == 422
    assert response.get_json()["code"] == "DAILY_LIMIT_EXCEEDED"
    assert get_balance(client, ANNA_ID) == "900.00"
