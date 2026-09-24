"""Tests for the store module."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from knbn.model.store import (
    StoreLockedError,
    TaskNotFoundError,
    add_task,
    delete_task,
    delete_task_by_id,
    ensure_data_dir,
    find_task_by_id,
    get_notes_path,
    load_tasks,
    notes_exist,
    open_notes_in_editor,
    save_tasks,
    update_task,
    update_task_by_id,
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
    return Task(**defaults)


def test_ensure_data_dir_creates_structure(tmp_path: Path) -> None:
    data_dir = tmp_path / 'knbn'
    ensure_data_dir(data_dir)
    assert data_dir.is_dir()
    assert (data_dir / 'tasks.csv').exists()
    assert (data_dir / 'notes').is_dir()
    assert (data_dir / 'settings.json').exists()


def test_ensure_data_dir_idempotent(tmp_path: Path) -> None:
    data_dir = tmp_path / 'knbn'
    ensure_data_dir(data_dir)
    ensure_data_dir(data_dir)  # second call must not raise


def test_ensure_data_dir_preserves_existing_settings(tmp_path: Path) -> None:
    data_dir = tmp_path / 'knbn'
    ensure_data_dir(data_dir)
    (data_dir / 'settings.json').write_text(
        '{"app": {"theme": "light"}}', encoding='utf-8'
    )
    ensure_data_dir(data_dir)
    assert '"light"' in (data_dir / 'settings.json').read_text()


def test_csv_has_header_after_init(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    content = (tmp_path / 'tasks.csv').read_text()
    assert content.startswith(
        'ID,DateTimeCreated,DateTimeEdited,DateTimeDue,Status,Priority,Category,Name'
    )


def test_load_tasks_wrong_schema(tmp_path: Path) -> None:
    csv_file = tmp_path / 'tasks.csv'
    csv_file.write_text(
        'Name,Category,Date Created,Delegated To,Due,Feedback From,Key Resource,Last edited time,Priority,Status\n'
    )
    with pytest.raises(ValueError, match='wrong schema'):
        load_tasks(tmp_path)

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
        assert orig.date_created == reloaded_task.date_created
        assert orig.date_modified == reloaded_task.date_modified
        assert orig.due == reloaded_task.due
        assert orig.key_resource == reloaded_task.key_resource
        assert orig.free_text_1 == reloaded_task.free_text_1
        assert orig.free_text_2 == reloaded_task.free_text_2
        assert orig.free_text_3 == reloaded_task.free_text_3


def test_atomic_save_uses_tmp_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ensure_data_dir(tmp_path)
    tasks = [_make_task()]
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
    saved = add_task(tmp_path, _make_task(title='Research feedback models'))
    path = get_notes_path(tmp_path, saved)
    assert path.suffix == '.md'
    assert saved.id in path.name


def test_notes_exist_false_when_absent(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='No notes here'))
    assert not notes_exist(tmp_path, saved)


def test_notes_exist_true_when_present(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='Has notes'))
    path = get_notes_path(tmp_path, saved)
    path.write_text('# Notes')
    assert notes_exist(tmp_path, saved)


def test_notes_path_stable_for_task(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='My task'))
    path1 = get_notes_path(tmp_path, saved)
    path2 = get_notes_path(tmp_path, saved)
    assert path1 == path2
    assert path1 == path2


def test_delete_task_removes_notes_file(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='Task with notes'))
    notes_path = get_notes_path(tmp_path, saved)
    notes_path.write_text('# My notes')
    assert notes_path.exists()
    delete_task(tmp_path, 0)
    assert not notes_path.exists()


def test_delete_task_without_notes_file(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    task = _make_task(title='Task without notes')
    add_task(tmp_path, task)
    delete_task(tmp_path, 0)  # must not raise
    assert load_tasks(tmp_path) == []


def test_open_notes_in_editor_creates_file_and_calls_editor(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='Editor task'))
    notes_path = get_notes_path(tmp_path, saved)

    def fake_run(cmd: list[str], **_: object) -> None:
        notes_path.write_text('some content')

    monkeypatch.setattr('knbn.model.store.subprocess.run', fake_run)
    open_notes_in_editor(tmp_path, saved)
    assert notes_path.exists()


def test_open_notes_in_editor_deletes_new_file_if_empty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='Blank task'))
    notes_path = get_notes_path(tmp_path, saved)

    monkeypatch.setattr('knbn.model.store.subprocess.run', lambda *a, **kw: None)
    open_notes_in_editor(tmp_path, saved)
    assert not notes_path.exists()


def test_open_notes_in_editor_deletes_new_file_if_whitespace_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='Whitespace task'))
    notes_path = get_notes_path(tmp_path, saved)

    def fake_run(cmd: list[str], **_: object) -> None:
        notes_path.write_text('  \n\t  ')

    monkeypatch.setattr('knbn.model.store.subprocess.run', fake_run)
    open_notes_in_editor(tmp_path, saved)
    assert not notes_path.exists()


def test_open_notes_in_editor_keeps_new_file_with_content(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='Content task'))
    notes_path = get_notes_path(tmp_path, saved)

    def fake_run(cmd: list[str], **_: object) -> None:
        notes_path.write_text('hello\n')

    monkeypatch.setattr('knbn.model.store.subprocess.run', fake_run)
    open_notes_in_editor(tmp_path, saved)
    assert notes_path.exists()
    assert notes_path.read_text().strip() == 'hello'


def test_open_notes_in_editor_preserves_existing_file_cleared_to_blank(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='Pre-existing task'))
    notes_path = get_notes_path(tmp_path, saved)
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    notes_path.write_text('original content')

    def fake_run(cmd: list[str], **_: object) -> None:
        notes_path.write_text('')

    monkeypatch.setattr('knbn.model.store.subprocess.run', fake_run)
    open_notes_in_editor(tmp_path, saved)
    assert notes_path.exists()


# --- New tests for IDs, locking, ID-based CRUD, db_version ---


def test_fixture_tasks_have_ids() -> None:
    tasks = load_tasks(FIXTURE_CSV.parent)
    assert all(t.id for t in tasks), 'All fixture tasks should have non-empty IDs'


def test_load_tasks_ids_are_8_chars() -> None:
    tasks = load_tasks(FIXTURE_CSV.parent)
    for task in tasks:
        assert len(task.id) == 8


def test_add_task_returns_task_with_id(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='ID task'))
    assert saved.id
    assert len(saved.id) == 8


def test_save_tasks_assigns_ids_to_tasks_without_id(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    tasks = [_make_task(title='No ID')]
    assert tasks[0].id == ''
    saved = save_tasks(tmp_path, tasks)
    assert saved[0].id
    reloaded = load_tasks(tmp_path)
    assert reloaded[0].id == saved[0].id


def test_save_tasks_preserves_existing_ids(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    tasks = [_make_task(title='With ID')]
    saved = save_tasks(tmp_path, tasks)
    original_id = saved[0].id
    saved2 = save_tasks(tmp_path, load_tasks(tmp_path))
    assert saved2[0].id == original_id


def test_round_trip_preserves_id(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    original = load_tasks(FIXTURE_CSV.parent)
    save_tasks(tmp_path, original)
    reloaded = load_tasks(tmp_path)
    for orig, rl in zip(original, reloaded):
        assert orig.id == rl.id


def test_legacy_csv_gets_ids_on_first_write(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    legacy_header = 'DateTimeCreated,DateTimeEdited,DateTimeDue,Status,Priority,Category,Name,FreeText1,FreeText2,FreeText3,KeyResource\n'
    legacy_row = '2026-07-01 14:27,2026-07-01 14:27,,Todo,Medium,Ideas,Old task,,,,\n'
    (tmp_path / 'tasks.csv').write_text(legacy_header + legacy_row)
    tasks = load_tasks(tmp_path)
    assert tasks[0].id == ''
    save_tasks(tmp_path, tasks)
    migrated = load_tasks(tmp_path)
    assert migrated[0].id
    assert len(migrated[0].id) == 8


def test_notes_migration_renames_slug_file_to_id(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    # Write a legacy CSV and a slug-named notes file
    legacy_header = 'DateTimeCreated,DateTimeEdited,DateTimeDue,Status,Priority,Category,Name,FreeText1,FreeText2,FreeText3,KeyResource\n'
    legacy_row = '2026-07-01 14:27,2026-07-01 14:27,,Todo,Medium,Ideas,Old task,,,,\n'
    (tmp_path / 'tasks.csv').write_text(legacy_header + legacy_row)
    notes_dir = tmp_path / 'notes'
    notes_dir.mkdir(exist_ok=True)
    slug_file = notes_dir / 'old-task.md'
    slug_file.write_text('# Some notes')
    # Trigger migration via ensure_data_dir
    ensure_data_dir(tmp_path)
    task = load_tasks(tmp_path)[0]
    assert task.id
    assert not slug_file.exists(), 'Slug-named file should have been renamed'
    id_file = notes_dir / f'{task.id}.md'
    assert id_file.exists(), 'ID-named file should exist after migration'
    assert id_file.read_text() == '# Some notes'


def test_notes_migration_skipped_when_no_notes_dir(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    legacy_header = 'DateTimeCreated,DateTimeEdited,DateTimeDue,Status,Priority,Category,Name,FreeText1,FreeText2,FreeText3,KeyResource\n'
    legacy_row = '2026-07-01 14:27,2026-07-01 14:27,,Todo,Medium,Ideas,No notes,,,,\n'
    (tmp_path / 'tasks.csv').write_text(legacy_header + legacy_row)
    (tmp_path / 'notes').rmdir()  # remove notes dir to hit the early-return branch
    ensure_data_dir(tmp_path)  # must not raise
    assert load_tasks(tmp_path)[0].id  # migration still happened for CSV


def test_migrate_notes_handles_slug_collision(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    legacy_header = 'DateTimeCreated,DateTimeEdited,DateTimeDue,Status,Priority,Category,Name,FreeText1,FreeText2,FreeText3,KeyResource\n'
    # Two tasks with the same title — second one gets slug-2.md
    row = '2026-07-01 14:27,2026-07-01 14:27,,Todo,Medium,Ideas,Same title,,,,\n'
    (tmp_path / 'tasks.csv').write_text(legacy_header + row + row)
    notes_dir = tmp_path / 'notes'
    notes_dir.mkdir(exist_ok=True)
    (notes_dir / 'same-title.md').write_text('first')
    (notes_dir / 'same-title-2.md').write_text('second')
    ensure_data_dir(tmp_path)
    tasks = load_tasks(tmp_path)
    assert tasks[0].id and tasks[1].id and tasks[0].id != tasks[1].id
    assert (notes_dir / f'{tasks[0].id}.md').read_text() == 'first'
    assert (notes_dir / f'{tasks[1].id}.md').read_text() == 'second'


def test_ensure_data_dir_ignores_corrupt_schema(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    # Write a completely invalid CSV header — migration should not crash
    (tmp_path / 'tasks.csv').write_text('Garbage,Header\n')
    ensure_data_dir(tmp_path)  # must not raise


def test_existing_slugs_empty_when_no_notes_dir(tmp_path: Path) -> None:
    from knbn.model.store import notes_id_set

    ensure_data_dir(tmp_path)
    (tmp_path / 'notes').rmdir()
    assert notes_id_set(tmp_path) == set()


def test_find_task_by_id_found(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='Findable'))
    found = find_task_by_id(tmp_path, saved.id)
    assert found.title == 'Findable'


def test_find_task_by_id_not_found(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    with pytest.raises(TaskNotFoundError, match='xxxxxxxx'):
        find_task_by_id(tmp_path, 'xxxxxxxx')


def test_update_task_by_id(tmp_path: Path) -> None:
    from dataclasses import replace

    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='Original'))
    updated = replace(saved, title='Updated')
    update_task_by_id(tmp_path, saved.id, updated)
    assert find_task_by_id(tmp_path, saved.id).title == 'Updated'


def test_update_task_by_id_not_found(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    with pytest.raises(TaskNotFoundError):
        update_task_by_id(tmp_path, 'xxxxxxxx', _make_task())


def test_delete_task_by_id(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='To delete'))
    delete_task_by_id(tmp_path, saved.id)
    assert load_tasks(tmp_path) == []


def test_delete_task_by_id_removes_notes(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    saved = add_task(tmp_path, _make_task(title='Notes task'))
    notes_path = get_notes_path(tmp_path, saved)
    notes_path.write_text('# Notes')
    delete_task_by_id(tmp_path, saved.id)
    assert not notes_path.exists()


def test_delete_task_by_id_not_found(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    with pytest.raises(TaskNotFoundError):
        delete_task_by_id(tmp_path, 'xxxxxxxx')


def test_ensure_data_dir_writes_db_version(tmp_path: Path) -> None:
    import json

    data_dir = tmp_path / 'knbn'
    ensure_data_dir(data_dir)
    settings = json.loads((data_dir / 'settings.json').read_text())
    assert 'db_version' in settings
    assert settings['db_version']


def test_save_tasks_updates_db_version_on_migration(tmp_path: Path) -> None:
    import json

    ensure_data_dir(tmp_path)
    legacy_header = 'DateTimeCreated,DateTimeEdited,DateTimeDue,Status,Priority,Category,Name,FreeText1,FreeText2,FreeText3,KeyResource\n'
    legacy_row = '2026-07-01 14:27,2026-07-01 14:27,,Todo,Medium,Ideas,Old task,,,,\n'
    (tmp_path / 'tasks.csv').write_text(legacy_header + legacy_row)
    tasks = load_tasks(tmp_path)
    save_tasks(tmp_path, tasks)
    settings = json.loads((tmp_path / 'settings.json').read_text())
    assert 'db_version' in settings


def test_save_tasks_raises_store_locked_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import knbn.model.store as store_module

    ensure_data_dir(tmp_path)
    monkeypatch.setattr(store_module, '_LOCK_TIMEOUT', 0.2)

    helper = (
        'from filelock import FileLock\n'
        'import sys, time\n'
        f"lock = FileLock(r'{tmp_path}/tasks.csv.lock')\n"
        'lock.acquire()\n'
        "sys.stdout.write('locked\\n')\n"
        'sys.stdout.flush()\n'
        'time.sleep(10)\n'
    )
    proc = subprocess.Popen(  # noqa: S603
        [sys.executable, '-c', helper],
        stdout=subprocess.PIPE,
    )
    assert proc.stdout is not None
    proc.stdout.readline()

    try:
        with pytest.raises(StoreLockedError):
            save_tasks(tmp_path, [])
    finally:
        proc.terminate()
        proc.wait()


def test_ensure_data_dir_writes_agents_md(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    agents_md = tmp_path / 'AGENTS.md'
    assert agents_md.exists()
    content = agents_md.read_text()
    assert 'knbn' in content
    assert 'github.com/BastiTee/knbn' in content


def test_ensure_data_dir_does_not_overwrite_agents_md(tmp_path: Path) -> None:
    ensure_data_dir(tmp_path)
    (tmp_path / 'AGENTS.md').write_text('custom agent instructions')
    ensure_data_dir(tmp_path)
    assert (tmp_path / 'AGENTS.md').read_text() == 'custom agent instructions'
