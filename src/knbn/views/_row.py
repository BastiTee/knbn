"""Focusable task row widget shared by list views."""

from __future__ import annotations

from rich.text import Text
from textual.events import Key
from textual.widgets import Static

from knbn.model.task import Task


class TaskRow(Static):
    """A single focusable row in a list view."""

    DEFAULT_CSS = """
    TaskRow {
        padding: 0 2;
    }
    TaskRow:focus {
        background: $accent-darken-1;
    }
    """

    def __init__(
        self, task_index: int, knbn_task: Task, row_text: str, **kwargs: object
    ) -> None:
        super().__init__(Text(row_text, no_wrap=True, overflow='ellipsis'), **kwargs)  # type: ignore[arg-type]
        self.task_index = task_index
        self.knbn_task = knbn_task
        self.can_focus = True

    def on_key(self, event: object) -> None:
        if isinstance(event, Key) and event.key in ('tab', 'shift+tab'):
            event.prevent_default()
            event.stop()
