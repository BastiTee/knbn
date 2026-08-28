"""Tests for the Task data model."""

import re
from datetime import datetime

from knbn.model.task import (
    Task,
    display_date,
    now_str,
    parse_datetime,
)


def test_task_required_fields_only() -> None:
    t = Task(
        title='My task',
        category='Ideas',
        status='Todo',
        priority='Medium',
        date_created='2026-07-01 14:27',
        date_modified='2026-07-01 14:27',
    )
    assert t.title == 'My task'
    assert t.category == 'Ideas'
    assert t.status == 'Todo'
    assert t.priority == 'Medium'
    assert t.due == ''
    assert t.key_resource == ''
    assert t.free_text_1 == ''
    assert t.free_text_2 == ''
    assert t.free_text_3 == ''


def test_task_all_fields() -> None:
    t = Task(
        title='Sync on headcount planning',
        category='People',
        status='Feedback',
        priority='High',
        date_created='2026-07-14 17:14',
        date_modified='2026-07-14 17:14',
        due='2026-07-17 09:00',
        key_resource='https://example.com/thread',
        free_text_1='Carol',
        free_text_2='',
        free_text_3='Extra',
    )
    assert t.free_text_1 == 'Carol'
    assert t.free_text_3 == 'Extra'
    assert t.key_resource == 'https://example.com/thread'
    assert t.due == '2026-07-17 09:00'


def test_free_text_fields_default_to_empty() -> None:
    t = Task(
        title='Test',
        category='Ideas',
        status='Todo',
        priority='Medium',
        date_created='2026-07-01 14:27',
        date_modified='2026-07-01 14:27',
    )
    assert t.free_text_1 == ''
    assert t.free_text_2 == ''
    assert t.free_text_3 == ''


def test_now_str_format() -> None:
    s = now_str()
    assert re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$', s), f'Unexpected format: {s}'


def test_parse_datetime_new_datetime() -> None:
    result = parse_datetime('2026-07-21 15:45')
    assert result is not None
    dt, has_time = result
    assert dt == datetime(2026, 7, 21, 15, 45)
    assert has_time is True


def test_parse_datetime_new_date_only() -> None:
    result = parse_datetime('2026-07-21')
    assert result is not None
    dt, has_time = result
    assert dt == datetime(2026, 7, 21, 0, 0)
    assert has_time is False


def test_parse_datetime_legacy_format() -> None:
    result = parse_datetime('July 21, 2026 3:45 PM')
    assert result is not None
    dt, has_time = result
    assert dt == datetime(2026, 7, 21, 15, 45)
    assert has_time is True


def test_parse_datetime_legacy_format_am() -> None:
    result = parse_datetime('July 8, 2026 7:36 AM')
    assert result is not None
    dt, has_time = result
    assert dt == datetime(2026, 7, 8, 7, 36)
    assert has_time is True


def test_parse_datetime_empty() -> None:
    assert parse_datetime('') is None


def test_parse_datetime_unrecognised() -> None:
    assert parse_datetime('not a date') is None


def test_display_date_datetime_input() -> None:
    assert display_date('2026-07-21 15:45') == '2026-07-21 15:45'


def test_display_date_date_only_input() -> None:
    assert display_date('2026-07-21') == '2026-07-21'


def test_display_date_legacy_format() -> None:
    assert display_date('July 21, 2026 3:45 PM') == '2026-07-21 15:45'


def test_display_date_empty() -> None:
    assert display_date('') == ''
