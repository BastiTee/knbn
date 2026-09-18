"""Tabular view — active tasks grouped by status."""

from __future__ import annotations

from dataclasses import replace

from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Static

from knbn.model.store import delete_task, load_tasks, update_task
from knbn.model.task import Task, display_date_only, now_str
from knbn.views._columns import format_row, header_text, title_col_width
from knbn.views._filter import task_matches
from knbn.views._row import TaskRow
from knbn.views._row_list import RowListView
from knbn.widgets._confirm import ConfirmDialog


def _sort_key(priority_rank: dict[str, int], task: Task) -> tuple[int, str]:
    return (priority_rank.get(task.priority, 99), task.date_modified)


class TabularView(RowListView):
    """Flat table of active tasks grouped by status."""

    BINDINGS = [
        Binding('d', 'mark_done', 'Done', show=False),
        Binding('delete', 'delete_task', 'Delete', show=False),
    ]

    @property
    def _search_query(self) -> str:
        return getattr(self.app, '_search_query', '')

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
    """

    def compose(self) -> ComposeResult:
        self._rows = []
        tw = title_col_width(self._view_width)
        yield Static(header_text(tw), classes='col-header-row')
        task_index = {id(t): i for i, t in enumerate(self._tasks)}

        board_config = self._board_config
        priority_rank = {p: i for i, p in enumerate(board_config.priorities)}

        for status in board_config.active_statuses:
            group = sorted(
                [
                    t
                    for t in self._tasks
                    if t.status == status and task_matches(t, self._search_query)
                ],
                key=lambda t: _sort_key(priority_rank, t),
            )
            if not group:
                continue
            yield Static(f'▼ {status}  {len(group)}', classes='group-header')
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

    def action_mark_done(self) -> None:
        if getattr(self.app, '_search_active', False):
            return
        i = self._focused_index()
        if i < 0:
            return
        row = self._rows[i]
        task = row.knbn_task
        idx = row.task_index
        terminal = self._board_config.default_terminal_status

        def on_confirm(confirmed: bool | None) -> None:
            if confirmed:
                updated = replace(task, status=terminal, date_modified=now_str())
                update_task(self.data_dir, idx, updated)
                self._tasks = load_tasks(self.data_dir)
                self._recompose_keeping_focus()

        self.app.push_screen(
            ConfirmDialog(f'Mark "{task.title}" as {terminal}?'), on_confirm
        )

    def action_delete_task(self) -> None:
        i = self._focused_index()
        if i < 0:
            return
        row = self._rows[i]
        task = row.knbn_task
        idx = row.task_index

        def on_confirm(confirmed: bool | None) -> None:
            if confirmed:
                delete_task(self.data_dir, idx)
                self._tasks = load_tasks(self.data_dir)
                self._recompose_keeping_focus()

        self.app.push_screen(ConfirmDialog(f'Delete "{task.title}"?'), on_confirm)
