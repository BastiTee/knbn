"""Help overlay widget."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Static

from knbn.config import BoardConfig

_HELP_GLOBAL = """\
[bold]Global[/bold]
  [cyan]q[/cyan] / [cyan]Ctrl+C[/cyan]  Quit
  [cyan]1[/cyan]           Kanban view
  [cyan]2[/cyan]           Tabular view
  [cyan]3[/cyan]           Closed view
  [cyan]a[/cyan]           Add task
  [cyan]?[/cyan]           This help
"""

_HELP_KANBAN_STATIC = """\
[bold]Kanban board[/bold]
  [cyan]← →[/cyan]         Move between columns
  [cyan]↑ ↓[/cyan]         Move between cards
  [cyan]Enter[/cyan]       Edit task
  [cyan]n[/cyan]           Open / create notes
"""

_HELP_KANBAN_TAIL = """\
  [cyan]Del[/cyan]         Delete task
  [cyan]PgUp / PgDn[/cyan]   Promote / demote priority
  [cyan]Shift+←→[/cyan]      Move to adjacent lane

[bold]Tabular / Closed views[/bold]
  [cyan]↑ ↓[/cyan]            Move between rows
  [cyan]PgUp / PgDn[/cyan]   Jump 10 rows
  [cyan]Enter[/cyan]          Edit task

[bold]Form[/bold]
  [cyan]Tab[/cyan]         Next field
  [cyan]Shift+Tab[/cyan]   Previous field
  [cyan]Esc[/cyan]         Cancel

[dim]Press Esc or ? to close[/dim]
"""


class HelpOverlay(ModalScreen[None]):
    """Key bindings help overlay."""

    @property
    def _board_config(self) -> BoardConfig:
        return self.app.board_config  # type: ignore[attr-defined,no-any-return]

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
        terminal = self._board_config.default_terminal_status
        mark_done_line = f'  [cyan]d[/cyan]           Mark {terminal}\n'
        help_text = (
            _HELP_GLOBAL + _HELP_KANBAN_STATIC + mark_done_line + _HELP_KANBAN_TAIL
        )
        yield Static(help_text, markup=True)

    def action_dismiss(self, result: None = None) -> None:  # type: ignore[override]
        self.dismiss(result)
