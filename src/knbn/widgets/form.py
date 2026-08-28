"""Add/edit task form overlay."""

from __future__ import annotations

import re
from dataclasses import replace
from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.events import Key
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select, Static

from knbn.config import BoardConfig
from knbn.model.store import add_task, update_task
from knbn.model.task import Task, now_str

_DUE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2}( \d{2}:\d{2})?)?$')


class DueInput(Input):
    """Due-date input that opens the date picker on Enter instead of submitting."""

    class OpenPicker(Message):
        """Posted when the user presses Enter in the due field."""

    async def _on_key(self, event: Key) -> None:
        if event.key == 'enter':
            event.stop()
            event.prevent_default()
            self.post_message(DueInput.OpenPicker())
        else:
            await super()._on_key(event)


class TaskForm(ModalScreen[None]):
    """Overlay form for creating or editing a task."""

    BINDINGS = [
        Binding('escape', 'cancel', 'Cancel', show=True),
        Binding('ctrl+s', 'save', 'Save', show=True),
    ]

    DEFAULT_CSS = """
    TaskForm {
        align: center middle;
    }
    TaskForm > Static {
        background: $surface;
        border: round $primary;
        padding: 1 3;
        width: 64;
        height: auto;
    }
    TaskForm Label {
        margin-top: 1;
    }
    TaskForm Select {
        width: 100%;
    }
    TaskForm Input {
        width: 100%;
    }
    TaskForm #form-buttons {
        margin-top: 1;
        layout: horizontal;
        height: auto;
    }
    TaskForm .due-error {
        color: $error;
        height: auto;
    }
    DueInput.has-error {
        border: tall $error;
    }
    """

    class TaskSaved(Message):
        """Posted after a task is successfully saved."""

    @property
    def _board_config(self) -> BoardConfig:
        return self.app.board_config  # type: ignore[attr-defined,no-any-return]

    def __init__(
        self,
        data_dir: Path,
        task: Task | None,
        task_index: int | None = None,
        initial_status: str | None = None,
        initial_priority: str | None = None,
        **kwargs: object,
    ) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self.data_dir = data_dir
        self.existing_task = task
        self.task_index = task_index
        self.initial_status = initial_status
        self.initial_priority = initial_priority

    def compose(self) -> ComposeResult:
        t = self.existing_task
        board_config = self._board_config
        all_statuses = board_config.all_statuses()
        priorities = board_config.priorities
        categories = [c.name for c in board_config.categories]

        default_status = t.status if t else (self.initial_status or all_statuses[0])
        default_priority = (
            t.priority
            if t
            else (self.initial_priority or priorities[len(priorities) // 2])
        )
        default_category = t.category if t else (categories[-1] if categories else '')

        with Static():
            yield Label(
                '[bold]Add Task[/bold]' if t is None else '[bold]Edit Task[/bold]',
                markup=True,
            )

            yield Label('Title')
            yield Input(value=t.title if t else '', id='f-title')

            yield Label('Status')
            status_opts = [(s, s) for s in all_statuses]
            yield Select(status_opts, value=default_status, id='f-status')

            yield Label('Priority')
            priority_opts = [(p, p) for p in priorities]
            yield Select(priority_opts, value=default_priority, id='f-priority')

            yield Label('Category')
            cat_opts = [(c, c) for c in categories]
            yield Select(cat_opts, value=default_category, id='f-category')

            yield Label('Due (YYYY-MM-DD or YYYY-MM-DD HH:MM, optional)')
            yield DueInput(value=t.due if t else '', id='f-due')
            yield Static('', id='due-error', classes='due-error')

            yield Label('Key Resource (URL, optional)')
            yield Input(value=t.key_resource if t else '', id='f-resource')

            for idx, label in board_config.active_free_text_fields():
                yield Label(f'{label} (optional)')
                val = getattr(t, f'free_text_{idx + 1}', '') if t else ''
                yield Input(value=val, id=f'f-free-{idx}')

            with Static(id='form-buttons'):
                yield Button('Save', id='save-btn', variant='primary')
                yield Button('Cancel', id='cancel-btn')

    def action_save(self) -> None:
        self._save()

    def action_cancel(self) -> None:
        self.dismiss()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'cancel-btn':
            self.dismiss()
        elif event.button.id == 'save-btn':
            self._save()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.input.id == 'f-due':
            event.input.remove_class('has-error')
            self.query_one('#due-error', Static).update('')

    def on_due_input_open_picker(self) -> None:
        from knbn.widgets.date_picker import DateTimePicker

        due_field = self.query_one('#f-due', DueInput)
        val = due_field.value.strip()
        due_error = self.query_one('#due-error', Static)
        if val and not _DUE_RE.match(val):
            due_error.update('Invalid format — use YYYY-MM-DD or YYYY-MM-DD HH:MM')
            due_field.add_class('has-error')
            return

        def _on_result(result: str | None) -> None:
            if result is not None:
                self.query_one('#f-due', DueInput).value = result

        self.app.push_screen(DateTimePicker(prefill=val or None), _on_result)

    def _save(self) -> None:
        title = self.query_one('#f-title', Input).value.strip()
        if not title:
            return

        def _sel_val(widget_id: str) -> str:
            sel = self.query_one(widget_id, Select)
            v = sel.value
            return str(v) if v is not None and v != Select.BLANK else ''

        status = _sel_val('#f-status') or self._board_config.active_statuses[0]
        priority = _sel_val('#f-priority') or self._board_config.priorities[0]
        categories = [c.name for c in self._board_config.categories]
        category = _sel_val('#f-category') or (categories[-1] if categories else '')
        due = self.query_one('#f-due', DueInput).value.strip()
        key_resource = self.query_one('#f-resource', Input).value.strip()

        free_text = ['', '', '']
        for idx, _ in self._board_config.active_free_text_fields():
            widget = self.query_one(f'#f-free-{idx}', Input)
            free_text[idx] = widget.value.strip()

        due_field = self.query_one('#f-due', DueInput)
        due_error = self.query_one('#due-error', Static)
        if due and not _DUE_RE.match(due):
            due_error.update('Invalid format — use YYYY-MM-DD or YYYY-MM-DD HH:MM')
            due_field.add_class('has-error')
            return
        due_field.remove_class('has-error')
        due_error.update('')

        now = now_str()

        if self.existing_task is not None and self.task_index is not None:
            updated = replace(
                self.existing_task,
                title=title,
                status=status,
                priority=priority,
                category=category,
                due=due,
                key_resource=key_resource,
                free_text_1=free_text[0],
                free_text_2=free_text[1],
                free_text_3=free_text[2],
                date_modified=now,
            )
            update_task(self.data_dir, self.task_index, updated)
        else:
            new_task = Task(
                title=title,
                category=category,
                status=status,
                priority=priority,
                date_created=now,
                date_modified=now,
                due=due,
                key_resource=key_resource,
                free_text_1=free_text[0],
                free_text_2=free_text[1],
                free_text_3=free_text[2],
            )
            add_task(self.data_dir, new_task)

        self.post_message(TaskForm.TaskSaved())
        self.dismiss()
