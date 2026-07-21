"""Closed view — terminal-status tasks grouped by ISO calendar week."""

from __future__ import annotations

import calendar
from datetime import date, datetime
from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Static

from knbn.model.task import STATUS_TERMINAL, Task
from knbn.views._columns import HEADER_TEXT, _date_only, format_row
from knbn.views._row import TaskRow
from knbn.views._row_list import RowListView


def _parse_modified(s: str) -> datetime | None:
    for fmt in ('%B %d, %Y %I:%M %p', '%B  %d, %Y %I:%M %p'):
        try:
            return datetime.strptime(s.strip(), fmt)
        except ValueError:
            continue
    return None


def _week_range_label(when: datetime) -> str:
    iso = when.isocalendar()
    year = iso[0]
    week = iso[1]
    monday = date.fromisocalendar(year, week, 1)
    sunday = date.fromisocalendar(year, week, 7)
    start_month = calendar.month_abbr[monday.month]
    end_month = calendar.month_abbr[sunday.month]
    if monday.month == sunday.month:
        return f'{start_month} {monday.day}–{sunday.day} {year}'
    return f'{start_month} {monday.day} – {end_month} {sunday.day} {year}'


class ClosedView(RowListView):
    """Terminal-status tasks grouped by ISO week of last-modified date."""

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

    def __init__(self, tasks: list[Task], data_dir: Path, **kwargs: object) -> None:
        super().__init__(tasks, data_dir, **kwargs)

    def compose(self) -> ComposeResult:
        self._rows = []
        yield Static(HEADER_TEXT, classes='col-header-row')
        task_index = {id(t): i for i, t in enumerate(self._tasks)}
        terminal = [t for t in self._tasks if t.status in STATUS_TERMINAL]

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
                idx = task_index[id(task)]
                due = _date_only(task.due) if task.due else ''
                row_text = format_row(
                    task.title,
                    task.status,
                    task.priority,
                    task.category,
                    _date_only(task.date_created),
                    _date_only(task.date_modified),
                    due,
                )
                row = TaskRow(idx, task, row_text)
                self._rows.append(row)
                yield row
