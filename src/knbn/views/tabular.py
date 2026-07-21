"""Tabular view — active tasks grouped by status."""

from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Static

from knbn.model.task import PRIORITY_VALUES, STATUS_ACTIVE, Task
from knbn.views._columns import HEADER_TEXT, display_date, format_row
from knbn.views._row import TaskRow
from knbn.views._row_list import RowListView

_PRIORITY_RANK = {p: i for i, p in enumerate(PRIORITY_VALUES)}


def _sort_key(task: Task) -> tuple[int, str]:
    return (_PRIORITY_RANK.get(task.priority, 99), task.date_modified)


class TabularView(RowListView):
    """Flat table of active tasks grouped by status."""

    DEFAULT_CSS = """
    TabularView {
        height: 1fr;
        overflow-y: auto;
        padding: 0 1;
    }
    .col-header-row {
        text-style: bold;
        padding: 0 1;
    }
    .group-header {
        text-style: bold;
        background: $primary-darken-2;
        padding: 0 1;
        margin-top: 1;
    }
    .group-header:first-child {
        margin-top: 0;
    }
    """

    def __init__(self, tasks: list[Task], data_dir: Path, **kwargs: object) -> None:
        super().__init__(tasks, data_dir, **kwargs)

    def compose(self) -> ComposeResult:
        self._rows = []
        yield Static(HEADER_TEXT, classes='col-header-row')
        task_index = {id(t): i for i, t in enumerate(self._tasks)}
        for status in STATUS_ACTIVE:
            group = sorted(
                [t for t in self._tasks if t.status == status],
                key=_sort_key,
            )
            if not group:
                continue
            yield Static(f'▼ {status}  {len(group)}', classes='group-header')
            for task in group:
                idx = task_index[id(task)]
                due = display_date(task.due) if task.due else ''
                row_text = format_row(
                    task.title,
                    task.status,
                    task.priority,
                    task.category,
                    display_date(task.date_created),
                    display_date(task.date_modified),
                    due,
                )
                row = TaskRow(idx, task, row_text)
                self._rows.append(row)
                yield row
