"""Help overlay widget."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Static

_HELP_TEXT = """\
[bold]Global[/bold]
  [cyan]q[/cyan] / [cyan]Ctrl+C[/cyan]  Quit
  [cyan]1[/cyan]           Kanban view
  [cyan]2[/cyan]           Tabular view
  [cyan]3[/cyan]           Done-by-week view
  [cyan]a[/cyan]           Add task
  [cyan]r[/cyan]           Reload from disk
  [cyan]?[/cyan]           This help

[bold]Kanban board[/bold]
  [cyan]← →[/cyan]         Move between columns
  [cyan]↑ ↓[/cyan]         Move between cards
  [cyan]Enter[/cyan]       Open task detail
  [cyan]e[/cyan]           Edit task
  [cyan]n[/cyan]           Open / create notes
  [cyan]d[/cyan]           Mark Done
  [cyan]x[/cyan]           Mark Stopped
  [cyan]g[/cyan]           Delegate task
  [cyan]m[/cyan]           Move to status
  [cyan]p[/cyan]           Change priority
  [cyan]Del[/cyan]         Delete task (confirm)
  [cyan]Space[/cyan]       Collapse / expand lane

[bold]Detail panel[/bold]
  [cyan]Esc[/cyan] / [cyan]q[/cyan]    Close panel
  [cyan]e[/cyan]           Edit task
  [cyan]n[/cyan]           Open notes
  [cyan]o[/cyan]           Open key resource URL
  [cyan]d[/cyan]           Delete task (confirm)

[bold]Tabular / Done views[/bold]
  [cyan]↑ ↓[/cyan]         Move between rows
  [cyan]Enter[/cyan]       Open task detail

[bold]Form[/bold]
  [cyan]Tab[/cyan]         Next field
  [cyan]Shift+Tab[/cyan]   Previous field
  [cyan]Esc[/cyan]         Cancel

[dim]Press Esc or ? to close[/dim]
"""


class HelpOverlay(ModalScreen[None]):
    """Key bindings help overlay."""

    BINDINGS = [
        Binding('escape', 'dismiss', 'Close'),
        Binding('question_mark', 'dismiss', 'Close'),
    ]

    DEFAULT_CSS = """
    HelpOverlay {
        align: center middle;
    }
    HelpOverlay > Static {
        background: $surface;
        border: round $primary;
        padding: 1 3;
        width: 52;
        height: auto;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static(_HELP_TEXT, markup=True)

    def action_dismiss(self, result: None = None) -> None:  # type: ignore[override]
        self.dismiss(result)
