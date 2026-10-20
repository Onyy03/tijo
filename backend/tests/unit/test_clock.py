from datetime import UTC, datetime

from app.clock import SystemClock


def test_should_return_current_utc_time_without_timezone():
    # given
    clock = SystemClock()
    before = datetime.now(UTC).replace(tzinfo=None)

    # when
    now = clock.now()

    # then
    after = datetime.now(UTC).replace(tzinfo=None)
    assert now.tzinfo is None
    assert before <= now <= after
