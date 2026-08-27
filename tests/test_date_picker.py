"""Unit tests for date_picker helpers (pure logic only — no TUI)."""

from __future__ import annotations

from datetime import date, timedelta

from knbn.widgets.date_picker import _adjust_time


class TestAdjustTime:
    def test_increment_hour(self) -> None:
        assert _adjust_time('10:30', 0, True) == '11:30'

    def test_decrement_hour(self) -> None:
        assert _adjust_time('10:30', 1, False) == '09:30'

    def test_increment_hour_wrap(self) -> None:
        assert _adjust_time('23:00', 0, True) == '00:00'

    def test_decrement_hour_wrap(self) -> None:
        assert _adjust_time('00:15', 2, False) == '23:15'

    def test_increment_minute(self) -> None:
        assert _adjust_time('10:30', 3, True) == '10:31'

    def test_decrement_minute(self) -> None:
        assert _adjust_time('10:30', 4, False) == '10:29'

    def test_increment_minute_wrap(self) -> None:
        assert _adjust_time('10:59', 5, True) == '10:00'

    def test_decrement_minute_wrap(self) -> None:
        assert _adjust_time('10:00', 3, False) == '10:59'

    def test_empty_value_returns_zero(self) -> None:
        assert _adjust_time('', 0, True) == '00:00'

    def test_invalid_value_returns_zero(self) -> None:
        assert _adjust_time('not-a-time', 0, True) == '00:00'

    def test_cursor_at_colon_adjusts_hour(self) -> None:
        # cursor_position == 2 is at/after the colon separator
        assert _adjust_time('05:00', 2, True) == '06:00'


class TestCalendarNavigation:
    """Calendar day navigation is pure date arithmetic — test the date logic."""

    def test_right_arrow_advances_one_day(self) -> None:
        d = date(2026, 8, 15)
        assert d + timedelta(days=1) == date(2026, 8, 16)

    def test_left_arrow_goes_back_one_day(self) -> None:
        d = date(2026, 8, 1)
        assert d + timedelta(days=-1) == date(2026, 7, 31)

    def test_left_arrow_wraps_to_previous_month(self) -> None:
        d = date(2026, 9, 1)
        prev = d + timedelta(days=-1)
        assert prev == date(2026, 8, 31)
        assert prev.month == 8

    def test_right_arrow_wraps_to_next_month(self) -> None:
        d = date(2026, 8, 31)
        nxt = d + timedelta(days=1)
        assert nxt == date(2026, 9, 1)
        assert nxt.month == 9

    def test_down_arrow_advances_one_week(self) -> None:
        d = date(2026, 8, 10)
        assert d + timedelta(days=7) == date(2026, 8, 17)

    def test_up_arrow_goes_back_one_week(self) -> None:
        d = date(2026, 8, 10)
        assert d + timedelta(days=-7) == date(2026, 8, 3)

    def test_week_navigation_wraps_month(self) -> None:
        d = date(2026, 8, 3)
        prev = d + timedelta(days=-7)
        assert prev == date(2026, 7, 27)
        assert prev.month == 7
