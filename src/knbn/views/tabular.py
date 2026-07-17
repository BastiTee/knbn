"""Tabular view — active tasks grouped by status."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static

from knbn.model.task import PRIORITY_VALUES, STATUS_ACTIVE, Task

_PRIORITY_RANK = {p: i for i, p in enumerate(PRIORITY_VALUES)}


def _sort_key(task: Task) -> tuple[int, str]:
    return (_PRIORITY_RANK.get(task.priority, 99), task.date_modified)


class TabularView(Widget):
    """Flat table of active tasks grouped by status."""

    DEFAULT_CSS = """
    TabularView {
        height: 1fr;
        overflow-y: auto;
        padding: 0 1;
    }
    .group-header {
        text-style: bold;
        background: $primary-darken-2;
        padding: 0 1;
        margin-top: 1;
    }
    .task-row {
        padding: 0 2;
    }
    """

    def __init__(self, tasks: list[Task], **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._tasks = tasks

    def compose(self) -> ComposeResult:
        for status in STATUS_ACTIVE:
            group = sorted(
                [t for t in self._tasks if t.status == status],
                key=_sort_key,
            )
            if not group:
                continue
            yield Static(f'▼ {status}  {len(group)}', classes='group-header')
            for task in group:
                due = task.due.split(' ')[0] if task.due else ''
                name = task.title if len(task.title) <= 40 else task.title[:39] + '…'
                row = f'  {name:<42} {task.priority:<8} {task.category:<14} {due}'
                yield Static(row, classes='task-row')
