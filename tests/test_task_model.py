"""Tests for the Task data model."""

import re
from datetime import datetime

from knbn.model.task import (
    DEFAULT_CATEGORIES,
    PRIORITY_VALUES,
    STATUS_ACTIVE,
    STATUS_TERMINAL,
    STATUS_VALUES,
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
    assert t.feedback_from == ''
    assert t.delegated_to == ''


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
        feedback_from='Carol',
        delegated_to='',
    )
    assert t.feedback_from == 'Carol'
    assert t.key_resource == 'https://example.com/thread'
    assert t.due == '2026-07-17 09:00'


def test_status_active_values() -> None:
    assert STATUS_ACTIVE == ['Todo', 'Now', 'Feedback']


def test_status_terminal_values() -> None:
    assert STATUS_TERMINAL == ['Done', 'Delegated', 'Stopped']


def test_status_values_combined() -> None:
    assert STATUS_VALUES == ['Todo', 'Now', 'Feedback', 'Done', 'Delegated', 'Stopped']


def test_priority_order() -> None:
    assert PRIORITY_VALUES == ['High', 'Medium', 'Low']


def test_default_categories_present() -> None:
    expected = [
        'People',
        'Hiring',
        'Strategy',
        'Product',
        'Engineering',
        'Work Life',
        'Ideas',
    ]
    assert expected == DEFAULT_CATEGORIES


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
