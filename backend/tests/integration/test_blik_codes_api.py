import re

from flask import Flask
from sqlalchemy import select

from app.codes.models import BlikCode, BlikCodeStatus
from app.extensions import db
from tests.integration.api_helpers import JAN_ID, generate_code


def stored_code_statuses(app: Flask) -> list[BlikCodeStatus]:
    with app.app_context():
        return list(db.session.scalars(select(BlikCode.status).order_by(BlikCode.id)))


def test_should_create_active_six_digit_code_valid_for_120_seconds(app, client):
    # given
    account_id = JAN_ID

    # when
    response = client.post(f"/api/accounts/{account_id}/blik-codes")

    # then
    assert response.status_code == 201
    body = response.get_json()
    assert re.fullmatch(r"\d{6}", body["code"])
    assert body["expires_at"] == "2026-11-02T12:02:00+00:00"
    assert stored_code_statuses(app) == [BlikCodeStatus.ACTIVE]


def test_should_cancel_previous_code_when_generating_new_one(app, client):
    # given
    generate_code(client, JAN_ID)

    # when
    generate_code(client, JAN_ID)

    # then
    assert stored_code_statuses(app) == [BlikCodeStatus.CANCELLED, BlikCodeStatus.ACTIVE]
