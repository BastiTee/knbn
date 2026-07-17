"""Task card widget."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Static

from knbn.model.task import Task

CATEGORY_COLORS: dict[str, str] = {
    'People': '#e879a0',
    'Hiring': '#f4a7b9',
    'Strategy': '#7ec8e3',
    'Product': '#5b9bd5',
    'Engineering': '#4dbfbf',
    'Work Life': '#f5a623',
    'Ideas': '#cccccc',
}
_DEFAULT_COLOR = '#888888'


def _parse_due(s: str) -> datetime | None:
    if not s:
        return None
    try:
        date_part = s.split(' ', maxsplit=1)[0]
        return datetime.strptime(date_part, '%d/%m/%Y')
    except ValueError:
        return None


class TaskCard(Static):
    """A card representing a single task on the Kanban board."""

    DEFAULT_CSS = """
    TaskCard {
        border: round $surface-darken-2;
        padding: 0 1;
        margin: 0 0 1 0;
        height: auto;
    }
    TaskCard:focus {
        border: round $primary;
    }
    """

    def __init__(self, knbn_task: Task, data_dir: Path, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self.knbn_task = knbn_task
        self.data_dir = data_dir
        self.can_focus = True

    def _notes_indicator(self) -> str:
        from knbn.model.store import notes_exist

        return ' [N]' if notes_exist(self.data_dir, self.knbn_task) else ''

    def _due_display(self) -> tuple[str, bool]:
        due = _parse_due(self.knbn_task.due)
        if due is None:
            return ('', False)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        overdue = due < today
        return (due.strftime('%d/%m/%Y'), overdue)

    def compose(self) -> ComposeResult:
        color = CATEGORY_COLORS.get(self.knbn_task.category, _DEFAULT_COLOR)
        notes = self._notes_indicator()
        title = self.knbn_task.title
        if len(title) > 30:
            title = title[:29] + '…'
        due_str, overdue = self._due_display()

        tag = f'[on {color}] {self.knbn_task.category} [/on {color}]'
        title_line = f'{title}{notes}'
        if due_str:
            due_markup = (
                f'[bold red]{due_str}[/bold red]'
                if overdue
                else f'[dim]{due_str}[/dim]'
            )
            bottom_line = f'{tag}  {due_markup}'
        else:
            bottom_line = tag
        yield Static(title_line, markup=False)
        yield Static(bottom_line, markup=True)

    def refresh_notes(self) -> None:
        self.refresh(layout=True)

    def on_key(self, event: object) -> None:
        from textual.events import Key

        if isinstance(event, Key) and event.key in ('tab', 'shift+tab'):
            event.prevent_default()
            event.stop()
