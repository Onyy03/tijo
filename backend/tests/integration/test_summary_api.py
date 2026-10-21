from tests.integration.api_helpers import ANNA_ID, JAN_ID, JAN_PHONE, create_pending_payment


def test_should_summarize_money_coming_in_and_out_of_account(client):
    # given
    payment_id = create_pending_payment(client, JAN_ID, amount="25.00")
    client.post(f"/api/payments/{payment_id}/confirm")
    client.post(
        "/api/transfers",
        json={
            "from_account_id": ANNA_ID,
            "to_phone_number": JAN_PHONE,
            "amount": "100.00",
            "title": "Zwrot",
        },
    )

    # when
    response = client.get(f"/api/accounts/{JAN_ID}/summary")

    # then
    assert response.status_code == 200
    assert response.get_json() == {
        "total_incoming": "100.00",
        "total_outgoing": "25.00",
        "operations_count": 2,
    }


def test_should_return_not_found_for_summary_of_unknown_account(client):
    # given
    unknown_account_id = 999

    # when
    response = client.get(f"/api/accounts/{unknown_account_id}/summary")

    # then
    assert response.status_code == 404
    assert response.get_json()["code"] == "ACCOUNT_NOT_FOUND"
