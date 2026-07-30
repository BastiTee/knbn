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

from knbn.model.store import (
    delete_task,
    load_tasks,
    open_notes_in_editor,
    save_tasks,
    update_task,
)
from knbn.model.task import (
    PRIORITY_VALUES,
    STATUS_VALUES,
    Task,
    now_str,
)
from knbn.widgets._confirm import ConfirmDialog
from knbn.widgets._modals import PromptModal, SelectModal
from knbn.widgets.card import TaskCard

_STATUS_ORDER = ['Todo', 'Now', 'Feedback']


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
        if isinstance(event, Key) and event.key in ('space', 'enter'):
            self._collapsed = not self._collapsed
            self.refresh()
            self.post_message(LaneHeader.Toggled(self._priority, self._collapsed))


class KanbanView(Widget):
    """3x3 Kanban board view."""

    BINDINGS = [
        Binding('left', 'focus_left', 'Left', show=False),
        Binding('right', 'focus_right', 'Right', show=False),
        Binding('up', 'focus_up', 'Up', show=False),
        Binding('down', 'focus_down', 'Down', show=False),
        Binding('pageup', 'move_up', 'Promote', show=False, priority=True),
        Binding('pagedown', 'move_down', 'Demote', show=False, priority=True),
        Binding('shift+left', 'move_left', 'Move Left', show=False, priority=True),
        Binding('shift+right', 'move_right', 'Move Right', show=False, priority=True),
        Binding('enter', 'open_detail', 'Detail', show=False),
        Binding('e', 'edit_task', 'Edit', show=False),
        Binding('n', 'open_notes', 'Notes', show=False),
        Binding('o', 'open_url', 'Open URL', show=False),
        Binding('d', 'mark_done', 'Done', show=False),
        Binding('x', 'mark_stopped', 'Stopped', show=False),
        Binding('g', 'delegate', 'Delegate', show=False),
        Binding('m', 'move_status', 'Move', show=False),
        Binding('p', 'change_priority', 'Priority', show=False),
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
        self._focused_row: dict[int, int] = {0: 0, 1: 0, 2: 0}

    def _tasks_for(self, status: str, priority: str) -> list[tuple[int, Task]]:
        return [
            (i, t)
            for i, t in enumerate(self._tasks)
            if t.status == status and t.priority == priority
        ]

    def _count_for_status(self, status: str) -> int:
        return sum(1 for t in self._tasks if t.status == status)

    def compose(self) -> ComposeResult:
        with Static(id='board-header'):
            for status in _STATUS_ORDER:
                count = self._count_for_status(status)
                yield Static(f'{status}  {count}', classes='col-header')

        with Container(id='board-body'):
            for col_idx, status in enumerate(_STATUS_ORDER):
                with Vertical(classes='board-col', id=f'col-{col_idx}'):
                    for priority in PRIORITY_VALUES:
                        yield LaneHeader(
                            priority,
                            collapsed=priority in self._collapsed,
                            id=f'lane-{col_idx}-{priority.lower()}',
                        )
                        if priority not in self._collapsed:
                            for idx, task in self._tasks_for(status, priority):
                                yield TaskCard(task, self.data_dir, id=f'card-{idx}')

        done = self._count_for_status('Done')
        delegated = self._count_for_status('Delegated')
        stopped = self._count_for_status('Stopped')
        yield Static(
            f'  Done {done:>6}   Delegated {delegated:>4}   Stopped {stopped:>4}',
            id='archive-bar',
        )

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

    def _get_cards_in_col(self, col_idx: int) -> list[TaskCard]:
        col = self.query_one(f'#col-{col_idx}')
        return list(col.query(TaskCard))

    def action_focus_left(self) -> None:
        current_row = self._focused_row.get(self._focused_col, 0)
        self._focused_col = max(0, self._focused_col - 1)
        self._focused_row[self._focused_col] = current_row
        self._focus_col_card()

    def action_focus_right(self) -> None:
        current_row = self._focused_row.get(self._focused_col, 0)
        self._focused_col = min(2, self._focused_col + 1)
        self._focused_row[self._focused_col] = current_row
        self._focus_col_card()

    def action_focus_up(self) -> None:
        r = self._focused_row.get(self._focused_col, 0)
        self._focused_row[self._focused_col] = max(0, r - 1)
        self._focus_col_card()

    def action_focus_down(self) -> None:
        cards = self._get_cards_in_col(self._focused_col)
        if not cards:
            return
        r = self._focused_row.get(self._focused_col, 0)
        self._focused_row[self._focused_col] = min(len(cards) - 1, r + 1)
        self._focus_col_card()

    def _focus_col_card(self) -> None:
        cards = self._get_cards_in_col(self._focused_col)
        if not cards:
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

    def action_open_detail(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        idx, task = ft
        from knbn.widgets.detail import TaskDetailPanel

        self.app.push_screen(TaskDetailPanel(idx, task, self.data_dir))

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

        def on_confirm(confirmed: bool | None) -> None:
            if confirmed:
                self._set_status('Done')

        self.app.push_screen(ConfirmDialog(f'Mark "{task.title}" as Done?'), on_confirm)

    def action_mark_stopped(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        _, task = ft

        def on_confirm(confirmed: bool | None) -> None:
            if confirmed:
                self._set_status('Stopped')

        self.app.push_screen(
            ConfirmDialog(f'Mark "{task.title}" as Stopped?'), on_confirm
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

    def action_delegate(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        idx, task = ft

        def on_name(name: str | None) -> None:
            if not name:
                return

            def on_confirm(confirmed: bool | None) -> None:
                if confirmed:
                    updated = replace(
                        task,
                        status='Delegated',
                        delegated_to=name,
                        date_modified=now_str(),
                    )
                    update_task(self.data_dir, idx, updated)
                    self._tasks = load_tasks(self.data_dir)
                    self.call_after_refresh(self.recompose)

            self.app.push_screen(
                ConfirmDialog(f'Delegate "{task.title}" to {name}?'), on_confirm
            )

        self.app.push_screen(PromptModal('Delegated To:'), on_name)

    def action_move_status(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        idx, task = ft
        options = [s for s in STATUS_VALUES if s != task.status]

        def on_status(new_status: str | None) -> None:
            if new_status:
                updated = replace(task, status=new_status)
                update_task(self.data_dir, idx, updated)
                self._tasks = load_tasks(self.data_dir)
                self.call_after_refresh(self.recompose)

        self.app.push_screen(SelectModal('Move to status:', options), on_status)

    def action_change_priority(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        idx, task = ft
        options = [p for p in PRIORITY_VALUES if p != task.priority]

        def on_priority(new_priority: str | None) -> None:
            if new_priority:
                updated = replace(task, priority=new_priority)
                update_task(self.data_dir, idx, updated)
                self._tasks = load_tasks(self.data_dir)
                self.call_after_refresh(self.recompose)

        self.app.push_screen(SelectModal('Change priority:', options), on_priority)

    def _move_task(self, updated: Task) -> None:
        """Save updated task, reload, then recompose and refocus by title."""
        ft = self._focused_task()
        if ft is None:
            return
        idx, _ = ft
        title = updated.title
        target_col = _STATUS_ORDER.index(updated.status)
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

    def action_move_up(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        idx, task = ft
        # Tasks in the same lane (same status+priority), ordered as they appear in the CSV
        lane = [
            i
            for i, t in enumerate(self._tasks)
            if t.status == task.status and t.priority == task.priority
        ]
        pos = lane.index(idx)
        if pos > 0:
            # Swap with the task above within the same lane
            tasks = list(self._tasks)
            tasks[lane[pos]], tasks[lane[pos - 1]] = (
                tasks[lane[pos - 1]],
                tasks[lane[pos]],
            )
            save_tasks(self.data_dir, tasks)
            self._tasks = load_tasks(self.data_dir)
            title = task.title
            col = self._focused_col

            def _refocus_up() -> None:
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
            self.call_after_refresh(_refocus_up)
        else:
            # Already at the top of the lane — promote to next higher priority
            pri_idx = PRIORITY_VALUES.index(task.priority)
            if pri_idx == 0:
                return
            self._move_task(replace(task, priority=PRIORITY_VALUES[pri_idx - 1]))

    def action_move_down(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        idx, task = ft
        lane = [
            i
            for i, t in enumerate(self._tasks)
            if t.status == task.status and t.priority == task.priority
        ]
        pos = lane.index(idx)
        if pos < len(lane) - 1:
            # Swap with the task below within the same lane
            tasks = list(self._tasks)
            tasks[lane[pos]], tasks[lane[pos + 1]] = (
                tasks[lane[pos + 1]],
                tasks[lane[pos]],
            )
            save_tasks(self.data_dir, tasks)
            self._tasks = load_tasks(self.data_dir)
            title = task.title
            col = self._focused_col

            def _refocus_down() -> None:
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
            self.call_after_refresh(_refocus_down)
        else:
            # Already at the bottom of the lane — demote to next lower priority
            pri_idx = PRIORITY_VALUES.index(task.priority)
            if pri_idx == len(PRIORITY_VALUES) - 1:
                return
            self._move_task(replace(task, priority=PRIORITY_VALUES[pri_idx + 1]))

    def action_move_left(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        _, task = ft
        col_idx = (
            _STATUS_ORDER.index(task.status) if task.status in _STATUS_ORDER else -1
        )
        if col_idx <= 0:
            return
        self._move_task(replace(task, status=_STATUS_ORDER[col_idx - 1]))

    def action_move_right(self) -> None:
        ft = self._focused_task()
        if ft is None:
            return
        _, task = ft
        col_idx = (
            _STATUS_ORDER.index(task.status) if task.status in _STATUS_ORDER else -1
        )
        if col_idx < 0 or col_idx >= len(_STATUS_ORDER) - 1:
            return
        self._move_task(replace(task, status=_STATUS_ORDER[col_idx + 1]))

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
