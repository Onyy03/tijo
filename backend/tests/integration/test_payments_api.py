from tests.integration.api_helpers import (
    ANNA_ID,
    JAN_ID,
    create_pending_payment,
    generate_code,
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
