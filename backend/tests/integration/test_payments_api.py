from tests.integration.api_helpers import (
    ANNA_ID,
    JAN_ID,
    PIOTR_ID,
    create_pending_payment,
    generate_code,
    get_balance,
    get_history,
    start_payment,
)


def test_should_create_pending_payment_when_code_is_valid(client):
    # given
    code = generate_code(client, JAN_ID)

    # when
    response = start_payment(client, code, amount="25.00", merchant_name="Żabka")

    # then
    assert response.status_code == 201
    body = response.get_json()
    assert (body["status"], body["amount"], body["merchant_name"]) == ("PENDING", "25.00", "Żabka")


def test_should_return_bad_request_when_code_format_is_invalid(client):
    # given
    malformed_code = "12ab56"

    # when
    response = start_payment(client, malformed_code)

    # then
    assert response.status_code == 400
    body = response.get_json()
    assert body["code"] == "VALIDATION_ERROR"
    assert body["errors"]["json"]["code"] == ["Kod BLIK musi mieć 6 cyfr"]


def test_should_return_not_found_when_code_does_not_exist(client):
    # given
    # no BLIK code has been generated yet

    # when
    response = start_payment(client, "999999")

    # then
    assert response.status_code == 404
    assert response.get_json()["code"] == "CODE_NOT_FOUND"


def test_should_reject_payment_when_code_has_expired(client, clock):
    # given
    code = generate_code(client, JAN_ID)
    clock.advance(seconds=121)

    # when
    response = start_payment(client, code)

    # then
    assert response.status_code == 422
    assert response.get_json()["code"] == "CODE_EXPIRED"


def test_should_reject_second_payment_with_the_same_code(client):
    # given
    code = generate_code(client, JAN_ID)
    assert start_payment(client, code).status_code == 201

    # when
    response = start_payment(client, code, amount="10.00", merchant_name="Biedronka")

    # then
    assert response.status_code == 422
    assert response.get_json()["code"] == "CODE_NOT_ACTIVE"


def test_should_list_new_payment_as_pending_only_for_code_owner(client):
    # given
    payment_id = create_pending_payment(client, JAN_ID)

    # when
    owner_pending = client.get(f"/api/accounts/{JAN_ID}/pending-payments").get_json()
    other_pending = client.get(f"/api/accounts/{ANNA_ID}/pending-payments").get_json()

    # then
    assert [payment["id"] for payment in owner_pending] == [payment_id]
    assert other_pending == []


def test_should_charge_account_and_record_history_when_payment_is_confirmed(client):
    # given
    payment_id = create_pending_payment(client, JAN_ID, amount="25.00")

    # when
    response = client.post(f"/api/payments/{payment_id}/confirm")

    # then
    assert response.status_code == 200
    assert response.get_json()["status"] == "CONFIRMED"
    assert client.get(f"/api/payments/{payment_id}").get_json()["status"] == "CONFIRMED"
    assert get_balance(client, JAN_ID) == "475.00"
    [entry] = get_history(client, JAN_ID)
    assert (entry["type"], entry["amount"], entry["description"]) == ("PAYMENT", "-25.00", "Żabka")


def test_should_keep_balance_when_confirming_without_sufficient_funds(client):
    # given
    payment_id = create_pending_payment(client, PIOTR_ID, amount="5.00")

    # when
    response = client.post(f"/api/payments/{payment_id}/confirm")

    # then
    assert response.status_code == 422
    assert response.get_json()["code"] == "INSUFFICIENT_FUNDS"
    assert get_balance(client, PIOTR_ID) == "0.00"
    assert client.get(f"/api/payments/{payment_id}").get_json()["status"] == "PENDING"


def test_should_mark_payment_as_rejected_without_charging_account(client):
    # given
    payment_id = create_pending_payment(client, JAN_ID)

    # when
    response = client.post(f"/api/payments/{payment_id}/reject")

    # then
    assert response.status_code == 200
    assert response.get_json()["status"] == "REJECTED"
    assert get_balance(client, JAN_ID) == "500.00"
    assert get_history(client, JAN_ID) == []


def test_should_refuse_confirmation_when_payment_has_expired(client, clock):
    # given
    payment_id = create_pending_payment(client, JAN_ID)
    clock.advance(seconds=121)

    # when
    response = client.post(f"/api/payments/{payment_id}/confirm")

    # then
    assert response.status_code == 422
    assert response.get_json()["code"] == "PAYMENT_EXPIRED"
    assert get_balance(client, JAN_ID) == "500.00"
    assert client.get(f"/api/accounts/{JAN_ID}/pending-payments").get_json() == []


def test_should_cancel_pending_payment_from_terminal(client):
    # given
    payment_id = create_pending_payment(client, JAN_ID)

    # when
    response = client.post(f"/api/payments/{payment_id}/cancel")

    # then
    assert response.status_code == 200
    assert response.get_json()["status"] == "CANCELLED"
    assert client.get(f"/api/accounts/{JAN_ID}/pending-payments").get_json() == []
    confirmation = client.post(f"/api/payments/{payment_id}/confirm")
    assert confirmation.get_json()["code"] == "PAYMENT_NOT_PENDING"
    assert get_balance(client, JAN_ID) == "500.00"
