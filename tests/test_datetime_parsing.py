"""Tests for Buienradar timestamp parsing compatibility."""

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from buienradar.buienradar_json import __to_localdatetime


AMSTERDAM = ZoneInfo("Europe/Amsterdam")


@pytest.mark.parametrize(
    ("timestamp", "expected"),
    [
        ("2019-02-03T19:20:00", datetime(2019, 2, 3, 19, 20, tzinfo=AMSTERDAM)),
        ("2026-10-13T01:50:00Z", datetime(2026, 10, 13, 1, 50, tzinfo=AMSTERDAM)),
        (
            "2026-10-13T01:50:00+02:00",
            datetime.fromisoformat("2026-10-13T01:50:00+02:00"),
        ),
        (
            "2026-10-13T01:50:00.123",
            datetime(2026, 10, 13, 1, 50, 0, 123000, tzinfo=AMSTERDAM),
        ),
    ],
)
def test_to_localdatetime_accepts_legacy_and_iso_timestamps(
    timestamp: str,
    expected: datetime,
) -> None:
    """Parse legacy timestamps, Z-suffixed timestamps, and explicit offsets."""
    assert __to_localdatetime(timestamp) == expected


@pytest.mark.parametrize("timestamp", ["", "not-a-date", "2026-99-99T01:50:00", None])
def test_to_localdatetime_returns_none_for_invalid_timestamps(
    timestamp: str | None,
) -> None:
    """Return None rather than raising for invalid or missing timestamps."""
    assert __to_localdatetime(timestamp) is None
