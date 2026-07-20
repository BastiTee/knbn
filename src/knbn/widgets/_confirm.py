"""Shared one-key confirmation dialog."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Static


class ConfirmDialog(ModalScreen[bool]):
    """Modal that asks a yes/no question and dismisses with True or False."""

    BINDINGS = [
        Binding('y', 'confirm', 'Yes'),
        Binding('n', 'cancel', 'No'),
        Binding('escape', 'cancel', 'No'),
    ]

    DEFAULT_CSS = """
    ConfirmDialog { align: center middle; }
    ConfirmDialog > Static {
        background: $surface; border: round $error;
        padding: 1 3; width: 44; height: auto;
    }
    """

    def __init__(self, message: str, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._message = message

    def compose(self) -> ComposeResult:
        yield Static(
            f'{self._message}\n\n[cyan]y[/cyan] Yes   [cyan]n[/cyan] / [cyan]Esc[/cyan] No',
            markup=True,
        )

    def action_confirm(self) -> None:
        self.dismiss(True)

    def action_cancel(self) -> None:
        self.dismiss(False)
