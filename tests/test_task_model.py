"""Tests for the Task data model."""

from knbn.model.task import (
    DEFAULT_CATEGORIES,
    PRIORITY_VALUES,
    STATUS_ACTIVE,
    STATUS_TERMINAL,
    STATUS_VALUES,
    Task,
)


def test_task_required_fields_only() -> None:
    t = Task(
        title='My task',
        category='Ideas',
        status='Todo',
        priority='Medium',
        date_created='July 1, 2026 2:27 PM',
        date_modified='July 1, 2026 2:27 PM',
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
        date_created='July 14, 2026 5:14 PM',
        date_modified='July 14, 2026 5:14 PM',
        due='17/07/2026 9:00 (GMT+2)',
        key_resource='https://example.com/thread',
        feedback_from='Carol',
        delegated_to='',
    )
    assert t.feedback_from == 'Carol'
    assert t.key_resource == 'https://example.com/thread'
    assert t.due == '17/07/2026 9:00 (GMT+2)'


def test_status_active_values() -> None:
    assert STATUS_ACTIVE == ['Todo', 'Now', 'Feedback']


def test_status_terminal_values() -> None:
    assert STATUS_TERMINAL == ['Done', 'Delegated', 'Stopped']


def test_status_values_combined() -> None:
    assert STATUS_VALUES == ['Todo', 'Now', 'Feedback', 'Done', 'Delegated', 'Stopped']
    assert len(STATUS_VALUES) == 6


def test_priority_order() -> None:
    assert PRIORITY_VALUES == ['High', 'Medium', 'Low']
    assert len(PRIORITY_VALUES) == 3


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
    assert len(DEFAULT_CATEGORIES) == 7
