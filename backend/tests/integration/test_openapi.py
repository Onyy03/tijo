def test_should_publish_openapi_specification_with_all_resources(client):
    # given
    expected_paths = {
        "/api/accounts",
        "/api/accounts/{account_id}/blik-codes",
        "/api/payments",
        "/api/payments/{payment_id}/confirm",
        "/api/transfers",
        "/api/accounts/{account_id}/history",
    }

    # when
    response = client.get("/api/openapi.json")

    # then
    assert response.status_code == 200
    specification = response.get_json()
    assert specification["info"]["title"] == "MiniBlik API"
    assert expected_paths <= set(specification["paths"])


def test_should_serve_swagger_ui_page(client):
    # given
    docs_url = "/api/docs"

    # when
    response = client.get(docs_url)

    # then
    assert response.status_code == 200
    assert response.content_type.startswith("text/html")
    assert "swagger-ui" in response.get_data(as_text=True)
