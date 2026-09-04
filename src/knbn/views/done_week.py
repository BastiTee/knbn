"""Closed view — terminal-status tasks grouped by ISO calendar week."""

from __future__ import annotations

import calendar
from datetime import date

from textual.app import ComposeResult
from textual.events import Resize
from textual.widgets import Static

from knbn.config import BoardConfig
from knbn.model.task import Task, display_date_only, parse_datetime
from knbn.views._columns import format_row, header_text, title_col_width
from knbn.views._row import TaskRow
from knbn.views._row_list import RowListView


def _week_range_label(iso_year: int, iso_week: int) -> str:
    monday = date.fromisocalendar(iso_year, iso_week, 1)
    sunday = date.fromisocalendar(iso_year, iso_week, 7)
    start_month = calendar.month_abbr[monday.month]
    end_month = calendar.month_abbr[sunday.month]
    if monday.month == sunday.month:
        return f'{start_month} {monday.day}–{sunday.day} {iso_year}'
    return f'{start_month} {monday.day} – {end_month} {sunday.day} {iso_year}'


class ClosedView(RowListView):
    """Terminal-status tasks grouped by ISO week of last-modified date."""

    @property
    def _board_config(self) -> BoardConfig:
        return self.app.board_config  # type: ignore[attr-defined,no-any-return]

    DEFAULT_CSS = """
    ClosedView {
        height: 1fr;
        overflow-y: auto;
        padding: 0 1;
    }
    .col-header-row {
        text-style: bold;
        padding: 0 1;
    }
    .week-header {
        text-style: bold;
        background: $primary-darken-2;
        padding: 0 1;
        margin-top: 1;
    }
    """

    def on_resize(self, event: Resize) -> None:
        self._recompose_keeping_focus()

    def compose(self) -> ComposeResult:
        self._rows = []
        tw = title_col_width(self._view_width)
        yield Static(header_text(tw), classes='col-header-row')
        task_index = {id(t): i for i, t in enumerate(self._tasks)}
        terminal_statuses = self._board_config.terminal_statuses
        terminal = [t for t in self._tasks if t.status in terminal_statuses]

        weeks: dict[tuple[int, int], list[Task]] = {}
        for task in terminal:
            result = parse_datetime(task.date_modified)
            if result is None:
                key = (0, 0)
            else:
                dt, _ = result
                iso = dt.isocalendar()
                key = (iso[0], iso[1])
            weeks.setdefault(key, []).append(task)

        for week_key in sorted(weeks.keys(), reverse=True):
            group = weeks[week_key]
            if week_key != (0, 0):
                label = _week_range_label(week_key[0], week_key[1])
            else:
                label = 'Unknown week'
            yield Static(f'▼ {label}  {len(group)}', classes='week-header')
            for task in group:
                idx = task_index[id(task)]
                due = display_date_only(task.due) if task.due else ''
                row_text = format_row(
                    task.title,
                    task.status,
                    task.priority,
                    task.category,
                    display_date_only(task.date_created),
                    display_date_only(task.date_modified),
                    due,
                    tw,
                )
                row = TaskRow(idx, task, row_text)
                self._rows.append(row)
                yield row
