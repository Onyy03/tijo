from collections.abc import Iterator
from datetime import datetime

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config import TestConfig
from app.extensions import db
from tests.fakes import MutableClock

START_TIME = datetime(2026, 11, 2, 12, 0, 0)


@pytest.fixture
def clock() -> MutableClock:
    return MutableClock(START_TIME)


@pytest.fixture
def app(clock: MutableClock) -> Iterator[Flask]:
    """A fresh application with its own in-memory database and the demo accounts."""
    app = create_app(TestConfig, clock=clock)
    yield app
    with app.app_context():
        db.engine.dispose()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
