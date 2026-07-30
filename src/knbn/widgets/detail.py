"""Task detail panel widget."""

from __future__ import annotations

import subprocess
from pathlib import Path

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Static

from knbn.model.store import delete_task, open_notes_in_editor
from knbn.model.task import Task
from knbn.widgets._confirm import ConfirmDialog


class TaskDetailPanel(ModalScreen[None]):
    """Full-detail overlay for a single task."""

    BINDINGS = [
        Binding('escape', 'dismiss', 'Close', show=True),
        Binding('q', 'dismiss', 'Close', show=False),
        Binding('e', 'edit', 'Edit', show=True),
        Binding('n', 'notes', 'Notes', show=True),
        Binding('o', 'open_resource', 'Open URL', show=True),
        Binding('delete,backspace', 'delete_task', 'Delete', show=True),
    ]

    DEFAULT_CSS = """
    TaskDetailPanel {
        align: center middle;
    }
    TaskDetailPanel > Static {
        background: $surface;
        border: round $primary;
        padding: 1 3;
        width: 60;
        height: auto;
    }
    """

    def __init__(
        self, task_index: int, knbn_task: Task, data_dir: Path, **kwargs: object
    ) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self.task_index = task_index
        self.knbn_task = knbn_task
        self.data_dir = data_dir

    def _render_text(self) -> str:
        t = self.knbn_task
        lines = [
            f'[bold]{t.title}[/bold]',
            '',
            f'[dim]Status:[/dim]     {t.status}',
            f'[dim]Priority:[/dim]   {t.priority}',
            f'[dim]Category:[/dim]   {t.category}',
            f'[dim]Due:[/dim]        {t.due or "—"}',
            f'[dim]Resource:[/dim]   {t.key_resource or "—"}',
            f'[dim]Feedback:[/dim]   {t.feedback_from or "—"}',
            f'[dim]Delegated:[/dim]  {t.delegated_to or "—"}',
            f'[dim]Created:[/dim]    {t.date_created}',
            f'[dim]Modified:[/dim]   {t.date_modified}',
            '',
            '[dim]e=edit  n=notes  o=open URL  Del=delete  Esc=close[/dim]',
        ]
        return '\n'.join(lines)

    def compose(self) -> ComposeResult:
        yield Static(self._render_text(), markup=True)

    def action_dismiss(self, result: None = None) -> None:  # type: ignore[override]
        self.dismiss(result)

    def action_edit(self) -> None:
        from knbn.widgets.form import TaskForm

        self.dismiss()
        self.app.push_screen(
            TaskForm(
                data_dir=self.data_dir, task=self.knbn_task, task_index=self.task_index
            )
        )

    def action_notes(self) -> None:
        with self.app.suspend():
            open_notes_in_editor(self.data_dir, self.knbn_task)

    def action_open_resource(self) -> None:
        if self.knbn_task.key_resource:
            subprocess.run(['open', self.knbn_task.key_resource], check=False)  # noqa: S603

    def action_delete_task(self) -> None:
        from knbn.app import KnbnApp

        def on_confirm(confirmed: bool | None) -> None:
            if confirmed:
                delete_task(self.data_dir, self.task_index)
                self.dismiss()
                app = self.app
                if isinstance(app, KnbnApp):
                    app.call_after_refresh(app.action_reload)

        self.app.push_screen(
            ConfirmDialog('[bold]Delete this task?[/bold]'), on_confirm
        )
