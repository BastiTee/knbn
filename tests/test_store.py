"""Tests for the store module."""

from __future__ import annotations

from pathlib import Path

import pytest

from knbn.model.store import (
    add_task,
    delete_task,
    ensure_data_dir,
    get_notes_path,
    load_tasks,
    notes_exist,
    save_tasks,
    update_task,
)
from knbn.model.task import Task

FIXTURE_CSV = Path(__file__).parent / 'fixtures' / 'tasks.csv'


def _make_task(**kwargs: str) -> Task:
    defaults: dict[str, str] = {
        'title': 'Test task',
        'category': 'Ideas',
        'status': 'Todo',
        'priority': 'Medium',
        'date_created': 'July 1, 2026 2:27 PM',
        'date_modified': 'July 1, 2026 2:27 PM',
    }
    defaults.update(kwargs)
    return Task(**defaults)  # type: ignore[arg-type]


def test_ensure_data_dir_creates_structure(tmp_path: Path) -> None:
    data_dir = tmp_path / 'knbn'
    ensure_data_dir(data_dir)
    assert data_dir.is_dir()
    assert (data_dir / 'tasks.csv').exists()
    assert (data_dir / 'notes').is_dir()


def test_ensure_data_dir_idempotent(tmp_path: Path) -> None:
    data_dir = tmp_path / 'knbn'
    ensure_data_dir(data_dir)
    ensure_data_dir(data_dir)  # second call must not raise


def test_csv_has_header_after_init(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    content = (tmp_path / 'tasks.csv').read_text()
    assert content.startswith('Name,Category,Date Created')


def test_load_tasks_from_fixture() -> None:
    tasks = load_tasks(FIXTURE_CSV.parent)
    assert len(tasks) == 16
    titles = [t.title for t in tasks]
    assert 'Research structured feedback models' in titles


def test_load_tasks_fixture_statuses() -> None:
    tasks = load_tasks(FIXTURE_CSV.parent)
    statuses = {t.status for t in tasks}
    assert 'Now' in statuses
    assert 'Done' in statuses
    assert 'Todo' in statuses


def test_round_trip(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    original = load_tasks(FIXTURE_CSV.parent)
    save_tasks(tmp_path, original)
    reloaded = load_tasks(tmp_path)
    assert len(reloaded) == len(original)
    for orig, reloaded_task in zip(original, reloaded):
        assert orig.title == reloaded_task.title
        assert orig.status == reloaded_task.status
        assert orig.priority == reloaded_task.priority
        assert orig.category == reloaded_task.category


def test_atomic_save_uses_tmp_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ensure_data_dir(tmp_path)
    tasks = [_make_task()]
    # Patch rename to capture that tmp file was used
    renamed_from: list[Path] = []
    original_rename = Path.rename

    def capturing_rename(self: Path, target: Path) -> Path:
        renamed_from.append(self)
        return original_rename(self, target)

    monkeypatch.setattr(Path, 'rename', capturing_rename)
    save_tasks(tmp_path, tasks)
    assert any('.tasks.csv.tmp' in str(p) for p in renamed_from)


def test_add_task(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    task = _make_task(title='Added task')
    add_task(tmp_path, task)
    tasks = load_tasks(tmp_path)
    assert len(tasks) == 1
    assert tasks[0].title == 'Added task'


def test_update_task(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    add_task(tmp_path, _make_task(title='Original'))
    updated = _make_task(title='Updated')
    update_task(tmp_path, 0, updated)
    tasks = load_tasks(tmp_path)
    assert tasks[0].title == 'Updated'


def test_delete_task(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    add_task(tmp_path, _make_task(title='First'))
    add_task(tmp_path, _make_task(title='Second'))
    delete_task(tmp_path, 0)
    tasks = load_tasks(tmp_path)
    assert len(tasks) == 1
    assert tasks[0].title == 'Second'


def test_notes_path_returns_path(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    task = _make_task(title='Research feedback models')
    path = get_notes_path(tmp_path, task)
    assert path.suffix == '.md'
    assert 'research-feedback-models' in path.name


def test_notes_exist_false_when_absent(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    task = _make_task(title='No notes here')
    assert not notes_exist(tmp_path, task)


def test_notes_exist_true_when_present(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    task = _make_task(title='Has notes')
    path = get_notes_path(tmp_path, task)
    path.write_text('# Notes')
    assert notes_exist(tmp_path, task)


def test_notes_path_consistent_for_existing_file(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    task = _make_task(title='My task')
    path1 = get_notes_path(tmp_path, task)
    path1.write_text('# Notes')
    path2 = get_notes_path(tmp_path, task)
    assert path1 == path2
