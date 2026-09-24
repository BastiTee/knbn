"""CSV-backed task persistence and notes file management."""

from __future__ import annotations

import csv
import os
import subprocess
from dataclasses import replace
from importlib.metadata import version
from pathlib import Path

from filelock import FileLock
from filelock import Timeout as FileLockTimeout

from knbn.model.slug import make_slug
from knbn.model.task import Task, generate_id

_CSV_FILENAME = 'tasks.csv'
_CSV_TMP_FILENAME = '.tasks.csv.tmp'
_NOTES_DIR = 'notes'
_LOCK_FILENAME = 'tasks.csv.lock'
_LOCK_TIMEOUT = 10.0

_CSV_FIELDNAMES = [
    'ID',
    'DateTimeCreated',
    'DateTimeEdited',
    'DateTimeDue',
    'Status',
    'Priority',
    'Category',
    'Name',
    'FreeText1',
    'FreeText2',
    'FreeText3',
    'KeyResource',
]

_OLD_CSV_FIELDNAMES = [
    'DateTimeCreated',
    'DateTimeEdited',
    'DateTimeDue',
    'Status',
    'Priority',
    'Category',
    'Name',
    'FreeText1',
    'FreeText2',
    'FreeText3',
    'KeyResource',
]


class StoreLockedError(ValueError):
    """Raised when the store lock cannot be acquired within the timeout."""


class TaskNotFoundError(ValueError):
    """Raised when a task with the given ID is not found in the store."""


def _csv_path(data_dir: Path) -> Path:
    return data_dir / _CSV_FILENAME


def _notes_dir(data_dir: Path) -> Path:
    return data_dir / _NOTES_DIR


def _detect_csv_schema(path: Path) -> bool:
    """Return True for the new 12-col schema, False for the legacy 11-col schema.

    Raises ValueError for any other header layout.
    """
    with path.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        found = next(reader, [])
    if found == _CSV_FIELDNAMES:
        return True
    if found == _OLD_CSV_FIELDNAMES:
        return False
    expected_str = ','.join(_CSV_FIELDNAMES)
    found_str = ','.join(found)
    raise ValueError(
        f'tasks.csv has wrong schema.\nExpected: {expected_str}\nFound:    {found_str}'
    )


def _task_to_row(task: Task) -> dict[str, str]:
    return {
        'ID': task.id,
        'DateTimeCreated': task.date_created,
        'DateTimeEdited': task.date_modified,
        'DateTimeDue': task.due,
        'Status': task.status,
        'Priority': task.priority,
        'Category': task.category,
        'Name': task.title,
        'FreeText1': task.free_text_1,
        'FreeText2': task.free_text_2,
        'FreeText3': task.free_text_3,
        'KeyResource': task.key_resource,
    }


def _row_to_task(row: dict[str, str]) -> Task:
    return Task(
        id=row.get('ID', ''),
        title=row['Name'],
        category=row['Category'],
        status=row['Status'],
        priority=row['Priority'],
        date_created=row['DateTimeCreated'],
        date_modified=row['DateTimeEdited'],
        due=row.get('DateTimeDue', ''),
        key_resource=row.get('KeyResource', ''),
        free_text_1=row.get('FreeText1', ''),
        free_text_2=row.get('FreeText2', ''),
        free_text_3=row.get('FreeText3', ''),
    )


def _ensure_ids(tasks: list[Task]) -> tuple[list[Task], bool]:
    """Assign IDs to any tasks that lack one. Returns (tasks, was_migrated)."""
    existing = {t.id for t in tasks if t.id}
    result: list[Task] = []
    migrated = False
    for t in tasks:
        if not t.id:
            new_id = generate_id()
            while new_id in existing:
                new_id = generate_id()
            existing.add(new_id)
            result.append(replace(t, id=new_id))
            migrated = True
        else:
            result.append(t)
    return result, migrated


def _write_db_version(data_dir: Path) -> None:
    from knbn.config import load_settings, save_settings

    settings = load_settings(data_dir)
    settings['db_version'] = version('knbn')
    save_settings(data_dir, settings)


def ensure_data_dir(data_dir: Path) -> None:
    from knbn.config import SETTINGS_DEFAULTS, save_settings

    data_dir.mkdir(parents=True, exist_ok=True)
    csv_file = _csv_path(data_dir)
    if not csv_file.exists():
        with csv_file.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=_CSV_FIELDNAMES)
            writer.writeheader()
    _notes_dir(data_dir).mkdir(exist_ok=True)
    settings_file = data_dir / 'settings.json'
    if not settings_file.exists():
        settings = dict(SETTINGS_DEFAULTS)
        save_settings(data_dir, settings)
    # Always ensure db_version is present and current
    _write_db_version(data_dir)
    # Eagerly migrate legacy CSV schema so IDs are assigned on startup
    if csv_file.exists():
        try:
            is_new_schema = _detect_csv_schema(csv_file)
        except ValueError:
            is_new_schema = True  # don't attempt migration on corrupt schema
        if not is_new_schema:
            old_tasks = load_tasks(data_dir)
            new_tasks = save_tasks(data_dir, old_tasks)
            _migrate_notes_files(data_dir, old_tasks, new_tasks)


def load_tasks(data_dir: Path) -> list[Task]:
    csv_file = _csv_path(data_dir)
    if not csv_file.exists():
        return []
    _detect_csv_schema(csv_file)
    with csv_file.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return [_row_to_task(row) for row in reader]


def save_tasks(data_dir: Path, tasks: list[Task]) -> list[Task]:
    lock_path = data_dir / _LOCK_FILENAME
    try:
        with FileLock(str(lock_path), timeout=_LOCK_TIMEOUT):
            tasks, migrated = _ensure_ids(tasks)
            if migrated:
                _write_db_version(data_dir)
            tmp_file = data_dir / _CSV_TMP_FILENAME
            with tmp_file.open('w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=_CSV_FIELDNAMES)
                writer.writeheader()
                for task in tasks:
                    writer.writerow(_task_to_row(task))
            tmp_file.rename(_csv_path(data_dir))
    except FileLockTimeout as exc:
        raise StoreLockedError(
            f'Could not acquire store lock within {_LOCK_TIMEOUT}s: {lock_path}'
        ) from exc
    return tasks


def add_task(data_dir: Path, task: Task) -> Task:
    tasks = load_tasks(data_dir)
    tasks.append(task)
    saved = save_tasks(data_dir, tasks)
    return saved[-1]


def update_task(data_dir: Path, index: int, task: Task) -> None:
    tasks = load_tasks(data_dir)
    tasks[index] = task
    save_tasks(data_dir, tasks)


def delete_task(data_dir: Path, index: int) -> None:
    tasks = load_tasks(data_dir)
    task = tasks[index]
    del tasks[index]
    save_tasks(data_dir, tasks)
    get_notes_path(data_dir, task).unlink(missing_ok=True)


def find_task_by_id(data_dir: Path, task_id: str) -> Task:
    tasks = load_tasks(data_dir)
    for task in tasks:
        if task.id == task_id:
            return task
    raise TaskNotFoundError(f"Task '{task_id}' not found")


def update_task_by_id(data_dir: Path, task_id: str, updated_task: Task) -> None:
    tasks = load_tasks(data_dir)
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = updated_task
            save_tasks(data_dir, tasks)
            return
    raise TaskNotFoundError(f"Task '{task_id}' not found")


def delete_task_by_id(data_dir: Path, task_id: str) -> None:
    tasks = load_tasks(data_dir)
    for i, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[i]
            save_tasks(data_dir, tasks)
            get_notes_path(data_dir, task).unlink(missing_ok=True)
            return
    raise TaskNotFoundError(f"Task '{task_id}' not found")


def _existing_slugs(data_dir: Path) -> set[str]:
    notes = _notes_dir(data_dir)
    if not notes.exists():
        return set()
    return {p.stem for p in notes.iterdir() if p.suffix == '.md'}


def notes_id_set(data_dir: Path) -> set[str]:
    """Return the set of note file stems (task IDs) under data_dir/notes."""
    return _existing_slugs(data_dir)


def get_notes_path(data_dir: Path, task: Task) -> Path:
    return _notes_dir(data_dir) / f'{task.id}.md'


def _migrate_notes_files(
    data_dir: Path, old_tasks: list[Task], new_tasks: list[Task]
) -> None:
    """Rename legacy slug-named notes files to ID-named ones.

    Processes tasks in CSV order to correctly resolve slug collisions the same
    way they were resolved when the files were originally created.
    """
    notes = _notes_dir(data_dir)
    if not notes.exists():
        return
    used_slugs: set[str] = set()
    for old_task, new_task in zip(old_tasks, new_tasks):
        base_slug = make_slug(old_task.title)
        if base_slug not in used_slugs:
            slug = base_slug
        else:
            n = 2
            while f'{base_slug}-{n}' in used_slugs:
                n += 1
            slug = f'{base_slug}-{n}'
        used_slugs.add(slug)
        old_path = notes / f'{slug}.md'
        new_path = notes / f'{new_task.id}.md'
        if old_path.exists() and not new_path.exists():
            old_path.rename(new_path)


def notes_exist(data_dir: Path, task: Task) -> bool:
    return get_notes_path(data_dir, task).exists()


def open_notes_in_editor(data_dir: Path, task: Task) -> None:
    notes_path = get_notes_path(data_dir, task)
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    already_existed = notes_path.exists()
    if not already_existed:
        notes_path.write_text('')
    editor = os.environ.get('EDITOR', 'nano')
    subprocess.run([editor, str(notes_path)], check=False)  # noqa: S603
    if (
        not already_existed
        and notes_path.exists()
        and not notes_path.read_text().strip()
    ):
        notes_path.unlink()
