"""Tests for the task search filter predicate."""

from knbn.model.task import Task
from knbn.views._filter import task_matches


def _task(**kwargs: str) -> Task:
    return Task(
        title=kwargs.get('title', ''),
        category=kwargs.get('category', ''),
        status=kwargs.get('status', 'Todo'),
        priority=kwargs.get('priority', 'Medium'),
        date_created=kwargs.get('date_created', '2024-01-01'),
        date_modified=kwargs.get('date_modified', '2024-01-01'),
        free_text_1=kwargs.get('free_text_1', ''),
        free_text_2=kwargs.get('free_text_2', ''),
        free_text_3=kwargs.get('free_text_3', ''),
    )


def test_empty_query_matches_everything() -> None:
    assert task_matches(_task(title='anything'), '')


def test_title_match() -> None:
    assert task_matches(_task(title='Fix the bug'), 'bug')


def test_title_no_match() -> None:
    assert not task_matches(_task(title='Deploy release'), 'bug')


def test_case_insensitive() -> None:
    assert task_matches(_task(title='Fix the BUG'), 'bug')
    assert task_matches(_task(title='fix the bug'), 'BUG')


def test_category_match() -> None:
    assert task_matches(_task(category='Engineering'), 'engi')


def test_free_text_1_match() -> None:
    assert task_matches(_task(free_text_1='alice'), 'alice')


def test_free_text_2_match() -> None:
    assert task_matches(_task(free_text_2='feedback from bob'), 'bob')


def test_free_text_3_match() -> None:
    assert task_matches(_task(free_text_3='notes here'), 'here')


def test_no_field_matches_returns_false() -> None:
    t = _task(
        title='Deploy', category='Ops', free_text_1='', free_text_2='', free_text_3=''
    )
    assert not task_matches(t, 'zzz')


def test_substring_in_middle() -> None:
    assert task_matches(_task(title='Very important task'), 'port')
