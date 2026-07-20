"""Shared base for list-style views (tabular, closed)."""

from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.events import Key
from textual.widget import Widget

from knbn.model.task import Task
from knbn.views._row import TaskRow


class RowListView(Widget):
    """Base widget for views that render a focusable list of TaskRow widgets."""

    BINDINGS = [
        Binding('up', 'cursor_up', 'Up', show=False),
        Binding('down', 'cursor_down', 'Down', show=False),
        Binding('pageup', 'cursor_up_fast', 'Up×10', show=False, priority=True),
        Binding('pagedown', 'cursor_down_fast', 'Down×10', show=False, priority=True),
        Binding('enter', 'open_detail', 'Open', show=False),
    ]

    def __init__(self, tasks: list[Task], data_dir: Path, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._tasks = tasks
        self.data_dir = data_dir
        self._rows: list[TaskRow] = []

    def compose(self) -> ComposeResult:
        raise NotImplementedError

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
