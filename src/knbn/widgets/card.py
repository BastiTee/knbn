"""Task card widget."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from textual.app import ComposeResult
from textual.events import Key
from textual.widgets import Static

from knbn.config import BoardConfig, get_app_setting
from knbn.model.task import Task, parse_datetime


def _parse_due(s: str) -> datetime | None:
    result = parse_datetime(s)
    return result[0] if result is not None else None


class TaskCard(Static):
    """A card representing a single task on the Kanban board."""

    DEFAULT_CSS = """
    TaskCard {
        border: round $surface-darken-2;
        padding: 0 1;
        margin: 0;
        height: auto;
    }
    TaskCard:focus {
        border: round $primary;
    }
    TaskCard.-deadline-warning {
        border-right: thick $warning;
    }
    """

    def __init__(self, knbn_task: Task, data_dir: Path, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self.knbn_task = knbn_task
        self.data_dir = data_dir
        self.can_focus = True

    @property
    def _board_config(self) -> BoardConfig:
        return self.app.board_config  # type: ignore[attr-defined,no-any-return]

    def _card_indicators(self) -> str:
        from knbn.model.store import notes_exist

        has_notes = notes_exist(self.data_dir, self.knbn_task)
        has_link = bool(self.knbn_task.key_resource)
        if has_notes and has_link:
            return ' ☰ ※'
        if has_notes:
            return ' ☰'
        if has_link:
            return ' ※'
        return ''

    def _due_display(self) -> tuple[str, bool]:
        due = _parse_due(self.knbn_task.due)
        if due is None:
            return ('', False)
        now = datetime.now()
        overdue = due < now
        if ' ' in self.knbn_task.due or 'T' in self.knbn_task.due:
            return (due.strftime('%Y-%m-%d %H:%M'), overdue)
        return (due.strftime('%Y-%m-%d'), overdue)

    def _is_deadline_warning(self) -> bool:
        due = _parse_due(self.knbn_task.due)
        if due is None:
            return False
        raw = get_app_setting(self.data_dir, 'deadline_warning_hours', '24')
        try:
            hours = int(raw)
        except (ValueError, TypeError):
            hours = 24
        return due <= datetime.now() + timedelta(hours=hours)

    def _title_for_width(self, reserved: int = 0) -> str:
        # inner width = widget width - 2 (border) - 2 (padding: 0 1)
        available = max(self.size.width - 4 - reserved, 4)
        title = self.knbn_task.title
        if len(title) > available:
            return title[: available - 1] + '…'
        return title

    def compose(self) -> ComposeResult:
        color = self._board_config.category_color(self.knbn_task.category)
        indicators = self._card_indicators()
        due_str, overdue = self._due_display()

        if due_str:
            reserved = 1 + len(due_str)
            title = self._title_for_width(reserved)
            inner_width = max(self.size.width - 4, 8)
            pad = inner_width - len(title) - len(indicators) - len(due_str)
            due_markup = (
                f'[bold red]{due_str}[/bold red]'
                if overdue
                else f'[dim]{due_str}[/dim]'
            )
            title_markup_line = f'{title}{indicators}{" " * max(pad, 1)}{due_markup}'
        else:
            title = self._title_for_width()
            title_markup_line = f'{title}{indicators}'

        tag = f'[on {color}] {self.knbn_task.category} [/on {color}]'
        yield Static(title_markup_line, markup=True)
        yield Static(tag, markup=True)

    def on_mount(self) -> None:
        if self._is_deadline_warning():
            self.add_class('-deadline-warning')
        else:
            self.remove_class('-deadline-warning')

    def refresh_notes(self) -> None:
        self.refresh(layout=True)

    def on_resize(self, event: object) -> None:
        self.call_after_refresh(self.recompose)

    def on_key(self, event: object) -> None:
        if isinstance(event, Key) and event.key in ('tab', 'shift+tab'):
            event.prevent_default()
            event.stop()
