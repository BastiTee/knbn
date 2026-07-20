"""Add/edit task form overlay."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select, Static

from knbn.model.store import add_task, update_task
from knbn.model.task import (
    DEFAULT_CATEGORIES,
    PRIORITY_VALUES,
    STATUS_VALUES,
    Task,
    now_str,
)


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
    """

    class TaskSaved(Message):
        """Posted after a task is successfully saved."""

    def __init__(
        self,
        data_dir: Path,
        task: Task | None,
        task_index: int | None = None,
        **kwargs: object,
    ) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self.data_dir = data_dir
        self.existing_task = task
        self.task_index = task_index

    def compose(self) -> ComposeResult:
        t = self.existing_task
        with Static():
            yield Label(
                '[bold]Add Task[/bold]' if t is None else '[bold]Edit Task[/bold]',
                markup=True,
            )

            yield Label('Title')
            yield Input(value=t.title if t else '', id='f-title')

            yield Label('Status')
            status_opts = [(s, s) for s in STATUS_VALUES]
            yield Select(status_opts, value=t.status if t else 'Todo', id='f-status')

            yield Label('Priority')
            priority_opts = [(p, p) for p in PRIORITY_VALUES]
            yield Select(
                priority_opts, value=t.priority if t else 'Medium', id='f-priority'
            )

            yield Label('Category')
            cat_opts = [(c, c) for c in DEFAULT_CATEGORIES]
            yield Select(cat_opts, value=t.category if t else 'Ideas', id='f-category')

            yield Label('Due (DD/MM/YYYY, optional)')
            yield Input(value=t.due if t else '', id='f-due')

            yield Label('Key Resource (URL, optional)')
            yield Input(value=t.key_resource if t else '', id='f-resource')

            yield Label('Feedback From (optional)')
            yield Input(value=t.feedback_from if t else '', id='f-feedback')

            yield Label('Delegated To (optional)')
            yield Input(value=t.delegated_to if t else '', id='f-delegated')

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

    def _save(self) -> None:
        title = self.query_one('#f-title', Input).value.strip()
        if not title:
            return

        def _sel_val(widget_id: str) -> str:
            sel = self.query_one(widget_id, Select)
            v = sel.value
            return str(v) if v is not None and v != Select.BLANK else ''

        status = _sel_val('#f-status') or 'Todo'
        priority = _sel_val('#f-priority') or 'Medium'
        category = _sel_val('#f-category') or 'Ideas'
        due = self.query_one('#f-due', Input).value.strip()
        key_resource = self.query_one('#f-resource', Input).value.strip()
        feedback_from = self.query_one('#f-feedback', Input).value.strip()
        delegated_to = self.query_one('#f-delegated', Input).value.strip()

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
                feedback_from=feedback_from,
                delegated_to=delegated_to,
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
                feedback_from=feedback_from,
                delegated_to=delegated_to,
            )
            add_task(self.data_dir, new_task)

        self.post_message(TaskForm.TaskSaved())
        self.dismiss()
