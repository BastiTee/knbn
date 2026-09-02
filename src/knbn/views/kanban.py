"""Kanban board view."""

from __future__ import annotations

import subprocess
from dataclasses import replace
from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.events import Key
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Static

from knbn.config import BoardConfig
from knbn.model.store import (
    delete_task,
    load_tasks,
    open_notes_in_editor,
    save_tasks,
    update_task,
)
from knbn.model.task import Task, now_str
from knbn.widgets._confirm import ConfirmDialog
from knbn.widgets.card import TaskCard


class LaneHeader(Static):
    """Collapsible swim-lane header."""

    class Toggled(Message):
        """Posted when the lane is collapsed/expanded."""

        def __init__(self, priority: str, collapsed: bool) -> None:
            super().__init__()
            self.priority = priority
            self.collapsed = collapsed

    can_focus = True

    DEFAULT_CSS = """
    LaneHeader {
        background: $surface-darken-1; padding: 0 1;
        height: 1; text-style: bold;
    }
    LaneHeader:focus { background: $accent; }
    """

    def __init__(
        self, priority: str, collapsed: bool = False, **kwargs: object
    ) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._priority = priority
        self._collapsed = collapsed

    def render(self) -> str:
        arrow = '▶' if self._collapsed else '▼'
        return f'{arrow} {self._priority}'

    def on_key(self, event: object) -> None:
        if isinstance(event, Key) and event.key == 'enter':
            self._collapsed = not self._collapsed
            self.refresh()
            self.post_message(LaneHeader.Toggled(self._priority, self._collapsed))


class KanbanView(Widget):
    """Config-driven Kanban board view."""

    BINDINGS = [
        Binding('left', 'focus_left', 'Left', show=False),
        Binding('right', 'focus_right', 'Right', show=False),
        Binding('up', 'focus_up', 'Up', show=False),
        Binding('down', 'focus_down', 'Down', show=False),
        Binding('pageup', 'move_up', 'Promote', show=False, priority=True),
        Binding('pagedown', 'move_down', 'Demote', show=False, priority=True),
        Binding('shift+left', 'move_left', 'Move Left', show=False, priority=True),
        Binding('shift+right', 'move_right', 'Move Right', show=False, priority=True),
        Binding('enter', 'edit_task', 'Edit', show=False),
        Binding('n', 'open_notes', 'Notes', show=False),
        Binding('o', 'open_url', 'Open URL', show=False),
        Binding('d', 'mark_done', 'Done', show=False),
        Binding('delete', 'delete_task', 'Delete', show=False),
        Binding('backspace', 'delete_task', 'Delete', show=False),
    ]

    DEFAULT_CSS = """
    KanbanView { height: 1fr; layout: vertical; }
    #board-header { height: 1; layout: horizontal; }
    .col-header {
        width: 1fr; text-align: center; text-style: bold;
        background: $primary-darken-2;
    }
    #board-body { height: 1fr; layout: horizontal; }
    .board-col {
        width: 1fr; height: 1fr;
        border-right: solid $surface-darken-2; overflow-y: auto;
    }
    #archive-bar { height: 1; background: $surface-darken-1; padding: 0 2; }
    """

    def __init__(self, tasks: list[Task], data_dir: Path, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._tasks = tasks
        self.data_dir = data_dir
        self._collapsed: set[str] = set()
        self._focused_col = 0
        self._focused_row: dict[int, int] = {}

    @property
    def _board_config(self) -> BoardConfig:
        return self.app.board_config  # type: ignore[attr-defined,no-any-return]

    def _tasks_for(self, status: str, priority: str) -> list[tuple[int, Task]]:
        return [
            (i, t)
            for i, t in enumerate(self._tasks)
            if t.status == status and t.priority == priority
        ]

    def _count_for_status(self, status: str) -> int:
        return sum(1 for t in self._tasks if t.status == status)

    def compose(self) -> ComposeResult:
        active_statuses = self._board_config.active_statuses
        priorities = self._board_config.priorities

        with Static(id='board-header'):
            for status in active_statuses:
                count = self._count_for_status(status)
                yield Static(f'{status}  {count}', classes='col-header')

        with Container(id='board-body'):
            for col_idx, status in enumerate(active_statuses):
                with Vertical(classes='board-col', id=f'col-{col_idx}'):
                    for priority in priorities:
                        yield LaneHeader(
                            priority,
                            collapsed=priority in self._collapsed,
                            id=f'lane-{col_idx}-{priority.lower().replace(" ", "-")}',
                        )
                        if priority not in self._collapsed:
                            for idx, task in self._tasks_for(status, priority):
                                yield TaskCard(task, self.data_dir, id=f'card-{idx}')

        terminal_statuses = self._board_config.terminal_statuses
        parts = [f'{s} {self._count_for_status(s):>6}' for s in terminal_statuses]
        yield Static('  ' + '   '.join(parts), id='archive-bar')

    async def on_lane_header_toggled(self, message: LaneHeader.Toggled) -> None:
        if message.collapsed:
            self._collapsed.add(message.priority)
        else:
            self._collapsed.discard(message.priority)
        await self.recompose()

    def _focused_card(self) -> TaskCard | None:
        focused = self.app.focused
        if isinstance(focused, TaskCard):
            return focused
        return None

    def _focused_task(self) -> tuple[int, Task] | None:
        card = self._focused_card()
        if card is None:
            return None
        card_id = card.id or ''
        if card_id.startswith('card-'):
            idx = int(card_id[5:])
            return idx, self._tasks[idx]
        return None

    def get_lane_context(self) -> tuple[str, str] | None:
        focused = self.app.focused
        active_statuses = self._board_config.active_statuses
        if isinstance(focused, TaskCard):
            t = focused.knbn_task
            return t.status, t.priority
        if isinstance(focused, LaneHeader):
            if self._focused_col < len(active_statuses):
                status = active_statuses[self._focused_col]
            else:
                status = active_statuses[0]
            return status, focused._priority
        return None

    def _get_cards_in_col(self, col_idx: int) -> list[TaskCard]:
        col = self.query_one(f'#col-{col_idx}')
        return list(col.query(TaskCard))

    def _get_focusable_in_col(self, col_idx: int) -> list[LaneHeader | TaskCard]:
        col = self.query_one(f'#col-{col_idx}')
        return [w for w in col.children if isinstance(w, (LaneHeader, TaskCard))]

    def action_focus_left(self) -> None:
        if self._focused_col <= 0:
            return
        focused = self.app.focused
        self._focused_col -= 1
        if isinstance(focused, LaneHeader):
            self._focus_same_priority_header(focused._priority)
        else:
            current_row = self._focused_row.get(self._focused_col + 1, 0)
            self._focused_row[self._focused_col] = current_row
            self._focus_col_card()

    def action_focus_right(self) -> None:
        n_cols = len(self._board_config.active_statuses)
        if self._focused_col >= n_cols - 1:
            return
        focused = self.app.focused
        self._focused_col += 1
        if isinstance(focused, LaneHeader):
            self._focus_same_priority_header(focused._priority)
        else:
            current_row = self._focused_row.get(self._focused_col - 1, 0)
            self._focused_row[self._focused_col] = current_row
            self._focus_col_card()

    def action_focus_up(self) -> None:
        focusable = self._get_focusable_in_col(self._focused_col)
        if not focusable:
            return
        focused = self.app.focused
        try:
            idx = focusable.index(focused)  # type: ignore[arg-type]
        except ValueError:
            idx = 0
        target = focusable[max(0, idx - 1)]
        target.focus()
        if isinstance(target, TaskCard):
            cards = self._get_cards_in_col(self._focused_col)
            if target in cards:
                self._focused_row[self._focused_col] = cards.index(target)

    def action_focus_down(self) -> None:
        focusable = self._get_focusable_in_col(self._focused_col)
        if not focusable:
            return
        focused = self.app.focused
        try:
            idx = focusable.index(focused)  # type: ignore[arg-type]
        except ValueError:
            idx = len(focusable) - 1
        target = focusable[min(len(focusable) - 1, idx + 1)]
        target.focus()
        if isinstance(target, TaskCard):
            cards = self._get_cards_in_col(self._focused_col)
            if target in cards:
                self._focused_row[self._focused_col] = cards.index(target)

    def _focus_same_priority_header(self, priority: str) -> None:
        col = self.query_one(f'#col-{self._focused_col}')
        for header in col.query(LaneHeader):
            if header._priority == priority:
                header.focus()
                return
        self._focus_col_card()

    def _focus_col_card(self) -> None:
        cards = self._get_cards_in_col(self._focused_col)
        if not cards:
            col = self.query_one(f'#col-{self._focused_col}')
            headers = list(col.query(LaneHeader))
            if headers:
                headers[0].focus()
            return
        row = min(self._focused_row.get(self._focused_col, 0), len(cards) - 1)
        self._focused_row[self._focused_col] = row
        cards[row].focus()

    def on_mount(self) -> None:
        self._focus_col_card()

    def on_key(self, event: object) -> None:
        if isinstance(event, Key) and event.key in ('tab', 'shift+tab'):
            event.prevent_default()
            event.stop()

    def action_edit_task(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        idx, task = ft
        from knbn.widgets.form import TaskForm

        self.app.push_screen(
            TaskForm(data_dir=self.data_dir, task=task, task_index=idx)
        )

    def action_open_notes(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        _, task = ft
        self._open_notes_for(task)

    def action_open_url(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        _, task = ft
        if task.key_resource:
            subprocess.run(['open', task.key_resource], check=False)  # noqa: S603

    def _open_notes_for(self, task: Task) -> None:
        with self.app.suspend():
            open_notes_in_editor(self.data_dir, task)
        self.call_after_refresh(self.recompose)

    def action_mark_done(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        _, task = ft
        terminal = self._board_config.default_terminal_status

        def on_confirm(confirmed: bool | None) -> None:
            if confirmed:
                self._set_status(terminal)

        self.app.push_screen(
            ConfirmDialog(f'Mark "{task.title}" as {terminal}?'), on_confirm
        )

    def _set_status(self, new_status: str) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        idx, task = ft
        updated = replace(task, status=new_status, date_modified=now_str())
        update_task(self.data_dir, idx, updated)
        self._tasks = load_tasks(self.data_dir)
        self.call_after_refresh(self.recompose)

    def _move_task(self, updated: Task) -> None:
        """Save updated task, reload, then recompose and refocus by title."""
        ft = self._focused_task()
        if ft is None:
            return
        idx, _ = ft
        title = updated.title
        active_statuses = self._board_config.active_statuses
        target_col = (
            active_statuses.index(updated.status)
            if updated.status in active_statuses
            else 0
        )
        update_task(self.data_dir, idx, updated)
        self._tasks = load_tasks(self.data_dir)

        def refocus() -> None:
            col_cards = self._get_cards_in_col(target_col)
            match_row = 0
            for i, card in enumerate(col_cards):
                card_id = card.id or ''
                if card_id.startswith('card-'):
                    card_idx = int(card_id[5:])
                    if (
                        card_idx < len(self._tasks)
                        and self._tasks[card_idx].title == title
                    ):
                        match_row = i
                        break
            self._focused_col = target_col
            self._focused_row[target_col] = match_row
            self._focus_col_card()

        self.call_after_refresh(self.recompose)
        self.call_after_refresh(refocus)

    def _swap_in_lane(self, direction: int) -> bool:
        """Swap the focused task one position within its lane.

        Returns True if the swap happened, False if the task is at the boundary.
        direction: -1 for up, +1 for down.
        """
        ft = self._focused_task()
        if ft is None:
            return False
        idx, task = ft
        lane = [
            i
            for i, t in enumerate(self._tasks)
            if t.status == task.status and t.priority == task.priority
        ]
        pos = lane.index(idx)
        target = pos + direction
        if not (0 <= target < len(lane)):
            return False
        tasks = list(self._tasks)
        tasks[lane[pos]], tasks[lane[target]] = tasks[lane[target]], tasks[lane[pos]]
        save_tasks(self.data_dir, tasks)
        self._tasks = load_tasks(self.data_dir)
        title = task.title
        col = self._focused_col

        def _refocus() -> None:
            col_cards = self._get_cards_in_col(col)
            for i, card in enumerate(col_cards):
                cid = card.id or ''
                if cid.startswith('card-'):
                    cidx = int(cid[5:])
                    if cidx < len(self._tasks) and self._tasks[cidx].title == title:
                        self._focused_row[col] = i
                        self._focus_col_card()
                        return

        self.call_after_refresh(self.recompose)
        self.call_after_refresh(_refocus)
        return True

    def action_move_up(self) -> None:
        if self._swap_in_lane(-1):
            return
        ft = self._focused_task()
        if ft is None:
            return
        _, task = ft
        priorities = self._board_config.priorities
        pri_idx = priorities.index(task.priority) if task.priority in priorities else -1
        if pri_idx <= 0:
            return
        self._move_task(replace(task, priority=priorities[pri_idx - 1]))

    def action_move_down(self) -> None:
        if self._swap_in_lane(1):
            return
        ft = self._focused_task()
        if ft is None:
            return
        _, task = ft
        priorities = self._board_config.priorities
        pri_idx = priorities.index(task.priority) if task.priority in priorities else -1
        if pri_idx < 0 or pri_idx >= len(priorities) - 1:
            return
        self._move_task(replace(task, priority=priorities[pri_idx + 1]))

    def action_move_left(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        _, task = ft
        active_statuses = self._board_config.active_statuses
        col_idx = (
            active_statuses.index(task.status) if task.status in active_statuses else -1
        )
        if col_idx <= 0:
            return
        self._move_task(replace(task, status=active_statuses[col_idx - 1]))

    def action_move_right(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        _, task = ft
        active_statuses = self._board_config.active_statuses
        col_idx = (
            active_statuses.index(task.status) if task.status in active_statuses else -1
        )
        if col_idx < 0 or col_idx >= len(active_statuses) - 1:
            return
        self._move_task(replace(task, status=active_statuses[col_idx + 1]))

    def action_delete_task(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        idx, task = ft

        def on_confirm(confirmed: bool | None) -> None:
            if confirmed:
                delete_task(self.data_dir, idx)
                self._tasks = load_tasks(self.data_dir)
                self.call_after_refresh(self.recompose)

        self.app.push_screen(ConfirmDialog(f'Delete "{task.title}"?'), on_confirm)
