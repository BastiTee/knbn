"""Done-by-week view — archived tasks grouped by ISO calendar week."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.widget import Widget
from textual.widgets import Static

from knbn.model.task import STATUS_TERMINAL, Task
from knbn.views._row import TaskRow

_DATE_FMT = '%B %d, %Y %I:%M %p'
_MONTH_ABBR = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
]


def _parse_modified(s: str) -> datetime | None:
    for fmt in ('%B %d, %Y %I:%M %p', '%B  %d, %Y %I:%M %p'):
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            continue
    return None


def _week_range_label(dt: datetime) -> str:
    iso = dt.isocalendar()
    year = iso[0]
    week = iso[1]
    # Monday of that ISO week
    import datetime as dt_module

    monday = dt_module.date.fromisocalendar(year, week, 1)
    sunday = dt_module.date.fromisocalendar(year, week, 7)
    start_month = _MONTH_ABBR[monday.month - 1]
    end_month = _MONTH_ABBR[sunday.month - 1]
    if monday.month == sunday.month:
        return f'{start_month} {monday.day}–{sunday.day} {year}'
    return f'{start_month} {monday.day} – {end_month} {sunday.day} {year}'


class DoneByWeekView(Widget):
    """Archived tasks grouped by ISO week of last-modified date."""

    BINDINGS = [
        Binding('up', 'cursor_up', 'Up', show=False),
        Binding('down', 'cursor_down', 'Down', show=False),
        Binding('enter', 'open_detail', 'Open', show=False),
    ]

    DEFAULT_CSS = """
    DoneByWeekView {
        height: 1fr;
        overflow-y: auto;
        padding: 0 1;
    }
    .week-header {
        text-style: bold;
        background: $surface-darken-1;
        padding: 0 1;
        margin-top: 1;
    }
    """

    def __init__(self, tasks: list[Task], data_dir: Path, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._tasks = tasks
        self.data_dir = data_dir
        self._rows: list[TaskRow] = []

    def compose(self) -> ComposeResult:
        self._rows = []
        terminal = [t for t in self._tasks if t.status in STATUS_TERMINAL]

        # Group by ISO week key (year, week_number) — sort key for ordering
        weeks: dict[tuple[int, int], list[Task]] = {}
        for task in terminal:
            dt = _parse_modified(task.date_modified)
            if dt is None:
                key = (0, 0)
            else:
                iso = dt.isocalendar()
                key = (iso[0], iso[1])
            weeks.setdefault(key, []).append(task)

        for week_key in sorted(weeks.keys(), reverse=True):
            group = weeks[week_key]
            sample_dt = _parse_modified(group[0].date_modified)
            if sample_dt and week_key != (0, 0):
                label = _week_range_label(sample_dt)
            else:
                label = 'Unknown week'
            yield Static(f'▼ {label}  {len(group)}', classes='week-header')
            for task in group:
                idx = self._tasks.index(task)
                name = task.title if len(task.title) <= 36 else task.title[:35] + '…'
                row_text = (
                    f'  {name:<38} {task.category:<14} {task.priority:<8}'
                    f' {task.date_modified:<22} {task.date_created}'
                )
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

    def action_open_detail(self) -> None:
        from knbn.widgets.detail import TaskDetailPanel

        i = self._focused_index()
        if i < 0:
            return
        row = self._rows[i]
        self.app.push_screen(
            TaskDetailPanel(row.task_index, row.knbn_task, self.data_dir)
        )
