"""CSV-backed task persistence and notes file management."""

from __future__ import annotations

import csv
from pathlib import Path

from knbn.model.slug import unique_slug
from knbn.model.task import Task

_CSV_FILENAME = 'tasks.csv'
_CSV_TMP_FILENAME = '.tasks.csv.tmp'
_NOTES_DIR = 'notes'

_CSV_FIELDNAMES = [
    'Name',
    'Category',
    'Date Created',
    'Delegated To',
    'Due',
    'Feedback From',
    'Key Resource',
    'Last edited time',
    'Priority',
    'Status',
]


def _csv_path(data_dir: Path) -> Path:
    return data_dir / _CSV_FILENAME


def _notes_dir(data_dir: Path) -> Path:
    return data_dir / _NOTES_DIR


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
        save_settings(data_dir, dict(SETTINGS_DEFAULTS))


def _task_to_row(task: Task) -> dict[str, str]:
    return {
        'Name': task.title,
        'Category': task.category,
        'Date Created': task.date_created,
        'Delegated To': task.delegated_to,
        'Due': task.due,
        'Feedback From': task.feedback_from,
        'Key Resource': task.key_resource,
        'Last edited time': task.date_modified,
        'Priority': task.priority,
        'Status': task.status,
    }


def _row_to_task(row: dict[str, str]) -> Task:
    return Task(
        title=row['Name'],
        category=row['Category'],
        status=row['Status'],
        priority=row['Priority'],
        date_created=row['Date Created'],
        date_modified=row['Last edited time'],
        due=row.get('Due', ''),
        key_resource=row.get('Key Resource', ''),
        feedback_from=row.get('Feedback From', ''),
        delegated_to=row.get('Delegated To', ''),
    )


def load_tasks(data_dir: Path) -> list[Task]:
    csv_file = _csv_path(data_dir)
    if not csv_file.exists():
        return []
    with csv_file.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return [_row_to_task(row) for row in reader]


def save_tasks(data_dir: Path, tasks: list[Task]) -> None:
    tmp_file = data_dir / _CSV_TMP_FILENAME
    with tmp_file.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=_CSV_FIELDNAMES)
        writer.writeheader()
        for task in tasks:
            writer.writerow(_task_to_row(task))
    tmp_file.rename(_csv_path(data_dir))


def add_task(data_dir: Path, task: Task) -> None:
    tasks = load_tasks(data_dir)
    tasks.append(task)
    save_tasks(data_dir, tasks)


def update_task(data_dir: Path, index: int, task: Task) -> None:
    tasks = load_tasks(data_dir)
    tasks[index] = task
    save_tasks(data_dir, tasks)


def delete_task(data_dir: Path, index: int) -> None:
    tasks = load_tasks(data_dir)
    del tasks[index]
    save_tasks(data_dir, tasks)


def _existing_slugs(data_dir: Path) -> set[str]:
    notes = _notes_dir(data_dir)
    if not notes.exists():
        return set()
    return {p.stem for p in notes.iterdir() if p.suffix == '.md'}


def get_notes_path(data_dir: Path, task: Task) -> Path:
    from knbn.model.slug import make_slug

    notes = _notes_dir(data_dir)
    base_slug = make_slug(task.title)
    candidate = notes / f'{base_slug}.md'
    if candidate.exists():
        return candidate
    slug = unique_slug(task.title, _existing_slugs(data_dir))
    return notes / f'{slug}.md'


def notes_exist(data_dir: Path, task: Task) -> bool:
    return get_notes_path(data_dir, task).exists()
