"""Tests for Buienradar timestamp parsing."""

from datetime import datetime
from zoneinfo import ZoneInfo

from buienradar.buienradar_json import __to_localdatetime


def test_z_suffix_uses_amsterdam_offset_for_timestamp_date():
    """Interpret Buienradar's Z-suffixed local clock value as Amsterdam time."""
    parsed_dt = __to_localdatetime("2026-10-16T02:10:00Z")

    assert parsed_dt == datetime(
        2026, 10, 16, 2, 10, tzinfo=ZoneInfo("Europe/Amsterdam")
    )
    assert parsed_dt.utcoffset().total_seconds() == 2 * 60 * 60


def test_explicit_offset_is_preserved():
    """Preserve an explicit ISO 8601 UTC offset."""
    parsed_dt = __to_localdatetime("2026-10-15T12:30:00+03:00")

    assert parsed_dt == datetime.fromisoformat("2026-10-15T12:30:00+03:00")
    assert parsed_dt.utcoffset().total_seconds() == 3 * 60 * 60


def test_timestamp_without_timezone_uses_amsterdam():
    """Interpret legacy naive timestamps in the Amsterdam timezone."""
    parsed_dt = __to_localdatetime("2026-10-15T12:30:00")

    assert parsed_dt == datetime(
        2026, 10, 15, 12, 30, tzinfo=ZoneInfo("Europe/Amsterdam")
    )


def test_invalid_timestamp_returns_none():
    """Return None for an invalid timestamp."""
    assert __to_localdatetime("not-a-timestamp") is None
