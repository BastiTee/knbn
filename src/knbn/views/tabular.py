"""Tabular view — active tasks grouped by status."""

from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Static

from knbn.model.task import PRIORITY_VALUES, STATUS_ACTIVE, Task
from knbn.views._row import TaskRow

_PRIORITY_RANK = {p: i for i, p in enumerate(PRIORITY_VALUES)}


def _sort_key(task: Task) -> tuple[int, str]:
    return (_PRIORITY_RANK.get(task.priority, 99), task.date_modified)


class TabularView(Widget):
    """Flat table of active tasks grouped by status."""

    BINDINGS = [
        Binding('up', 'cursor_up', 'Up', show=False),
        Binding('down', 'cursor_down', 'Down', show=False),
        Binding('pageup', 'cursor_up_fast', 'Up×10', show=False, priority=True),
        Binding('pagedown', 'cursor_down_fast', 'Down×10', show=False, priority=True),
        Binding('enter', 'open_detail', 'Open', show=False),
    ]

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
    .group-header:first-child {
        margin-top: 0;
    }
    """

    def __init__(self, tasks: list[Task], data_dir: Path, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._tasks = tasks
        self.data_dir = data_dir
        self._rows: list[TaskRow] = []

    def compose(self) -> ComposeResult:
        self._rows = []
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
                due = task.due.split(' ')[0] if task.due else ''
                name = task.title if len(task.title) <= 40 else task.title[:39] + '…'
                row_text = f'  {name:<42} {task.priority:<8} {task.category:<14} {due}'
                row = TaskRow(idx, task, row_text)
                self._rows.append(row)
                yield row

    def _focused_index(self) -> int:
        focused = self.app.focused
        for i, row in enumerate(self._rows):
            if row is focused:
                return i
        return -1

    def action_cursor_up(self) -> None:
        if not self._rows:
            return
        i = self._focused_index()
        self._rows[max(i - 1, 0)].focus()

    def action_cursor_down(self) -> None:
        if not self._rows:
            return
        i = self._focused_index()
        self._rows[min(i + 1, len(self._rows) - 1)].focus()

    def action_cursor_up_fast(self) -> None:
        if not self._rows:
            return
        i = self._focused_index()
        self._rows[max(i - 10, 0)].focus()

    def action_cursor_down_fast(self) -> None:
        if not self._rows:
            return
        i = self._focused_index()
        self._rows[min(i + 10, len(self._rows) - 1)].focus()

    def on_mount(self) -> None:
        if self._rows:
            self._rows[0].focus()

    def on_key(self, event: object) -> None:
        from textual.events import Key

        if isinstance(event, Key) and event.key in ('tab', 'shift+tab'):
            event.prevent_default()
            event.stop()

    def action_open_detail(self) -> None:
        from knbn.widgets.detail import TaskDetailPanel

        i = self._focused_index()
        if i < 0:
            return
        row = self._rows[i]
        self.app.push_screen(
            TaskDetailPanel(row.task_index, row.knbn_task, self.data_dir)
        )
