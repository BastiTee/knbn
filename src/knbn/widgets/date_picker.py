"""Date/time picker overlay widget."""

from __future__ import annotations

import calendar
import re
from datetime import date, timedelta

from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.events import Click, Key
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Static

_TIME_RE = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')
_CELL_W = 3  # chars per calendar cell


def _adjust_time(value: str, cursor_pos: int, up: bool) -> str:
    """Return a new HH:MM string with hour or minute incremented/decremented."""
    stripped = value.strip()
    if not re.match(r'^\d{2}:\d{2}$', stripped):
        return '00:00'
    h, m = int(stripped[:2]), int(stripped[3:])
    if cursor_pos <= 2:
        h = (h + (1 if up else -1)) % 24
    else:
        m = (m + (1 if up else -1)) % 60
    return f'{h:02d}:{m:02d}'


class CalendarGrid(Static):
    """Focusable calendar month grid rendered as Rich text."""

    class Confirmed(Message):
        """Posted when Enter is pressed or a day cell is double-clicked."""

    can_focus = True

    DEFAULT_CSS = """
    CalendarGrid {
        width: 23; height: 8;
    }
    CalendarGrid:focus { border: none; }
    """

    def __init__(self, selected: date, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._selected = selected

    @property
    def selected(self) -> date:
        return self._selected

    def _render_grid(self) -> Text:
        y, m = self._selected.year, self._selected.month
        today = date.today()
        t = Text(no_wrap=True)
        header = self._selected.strftime('%B %Y')
        t.append(f'{header:^23}\n', style='bold')
        t.append('  Mo Tu We Th Fr Sa Su\n', style='dim')
        rows = calendar.monthcalendar(y, m)
        while len(rows) < 6:
            rows.append([0, 0, 0, 0, 0, 0, 0])
        for week in rows:
            t.append('  ')
            for day in week:
                if day == 0:
                    t.append('   ')
                else:
                    d = date(y, m, day)
                    cell = f'{day:2d} '
                    if d == self._selected:
                        t.append(cell, style='bold reverse')
                    elif d == today:
                        t.append(cell, style='bold underline')
                    else:
                        t.append(cell)
            t.append('\n')
        return t

    def render(self) -> Text:
        return self._render_grid()

    def _navigate(self, delta: int) -> None:
        self._selected = self._selected + timedelta(days=delta)
        self.refresh()

    async def _on_key(self, event: Key) -> None:
        if event.key == 'left':
            event.stop()
            self._navigate(-1)
        elif event.key == 'right':
            event.stop()
            self._navigate(1)
        elif event.key == 'up':
            event.stop()
            self._navigate(-7)
        elif event.key == 'down':
            event.stop()
            self._navigate(7)
        elif event.key == 'enter':
            event.stop()
            self.post_message(CalendarGrid.Confirmed())

    def on_click(self, event: Click) -> None:
        col = (event.x - 2) // _CELL_W
        row = event.y - 2
        cal_rows = calendar.monthcalendar(self._selected.year, self._selected.month)
        if 0 <= row < len(cal_rows) and 0 <= col < 7:
            day = cal_rows[row][col]
            if day != 0:
                self._selected = date(self._selected.year, self._selected.month, day)
                self.refresh()
                if event.chain >= 2:
                    self.post_message(CalendarGrid.Confirmed())


class _TimeInput(Input):
    """Time input that increments/decrements hour/minute on up/down arrows."""

    async def _on_key(self, event: Key) -> None:
        if event.key in ('up', 'down'):
            event.stop()
            event.prevent_default()
            self.value = _adjust_time(
                self.value, self.cursor_position, event.key == 'up'
            )
        else:
            await super()._on_key(event)


class DateTimePicker(ModalScreen['str | None']):
    """Overlay date/time picker. Dismisses with a formatted date string or None."""

    BINDINGS = [
        Binding('escape', 'cancel', 'Cancel'),
    ]

    DEFAULT_CSS = """
    DateTimePicker { align: center middle; }
    DateTimePicker > Static#picker-shell {
        background: $surface;
        border: round $primary;
        padding: 1 2;
        width: 27;
        height: auto;
    }
    DateTimePicker Label { margin-top: 1; }
    DateTimePicker Input { width: 100%; }
    DateTimePicker .time-error { color: $error; height: auto; }
    """

    def __init__(self, prefill: str | None = None, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._initial_date = date.today()
        self._initial_time = ''
        if prefill:
            parts = prefill.split(' ', 1)
            try:
                self._initial_date = date.fromisoformat(parts[0])
            except ValueError:
                pass
            if len(parts) == 2:
                self._initial_time = parts[1]

    def compose(self) -> ComposeResult:
        with Static(id='picker-shell'):
            yield CalendarGrid(self._initial_date, id='cal-grid')
            yield Label('Time (HH:MM, optional)')
            yield _TimeInput(
                value=self._initial_time,
                placeholder='HH:MM',
                id='time-input',
            )
            yield Static('', id='time-error', classes='time-error')

    def on_calendar_grid_confirmed(self) -> None:
        self._confirm()

    def on_input_submitted(self) -> None:
        self._confirm()

    def action_cancel(self) -> None:
        self.dismiss(None)

    def _confirm(self) -> None:
        cal = self.query_one('#cal-grid', CalendarGrid)
        time_str = self.query_one('#time-input', _TimeInput).value.strip()
        error = self.query_one('#time-error', Static)
        if time_str:
            if not _TIME_RE.match(time_str):
                error.update('Invalid time — use HH:MM')
                return
            result = f'{cal.selected} {time_str}'
        else:
            result = str(cal.selected)
        error.update('')
        self.dismiss(result)
