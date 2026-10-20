def test_should_return_demo_accounts_when_listing_accounts(client):
    # given
    # the application created its demo accounts on start

    # when
    response = client.get("/api/accounts")

    # then
    assert response.status_code == 200
    assert [
        (account["owner_name"], account["phone_number"], account["balance"])
        for account in response.get_json()
    ] == [
        ("Jan Kowalski", "500100200", "500.00"),
        ("Anna Nowak", "600200300", "1500.00"),
        ("Piotr Zieliński", "700300400", "0.00"),
    ]


def test_should_return_not_found_when_account_does_not_exist(client):
    # given
    unknown_account_id = 999

    # when
    response = client.get(f"/api/accounts/{unknown_account_id}")

    # then
    assert response.status_code == 404
    assert response.get_json() == {"code": "ACCOUNT_NOT_FOUND", "message": "Nie znaleziono konta"}
