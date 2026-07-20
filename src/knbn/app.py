"""Textual TUI application."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from textual.app import App, ComposeResult, SystemCommand
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from knbn.model.store import ensure_data_dir, load_tasks
from knbn.model.task import Task


class KnbnApp(App[None]):
    """Terminal Kanban board."""

    TITLE = 'knbn'
    CSS = """
    Screen {
        background: $surface;
    }
    #view-container {
        height: 1fr;
    }
    """

    BINDINGS = [
        Binding('1', 'show_kanban', 'Kanban', show=True),
        Binding('2', 'show_tabular', 'Tabular', show=True),
        Binding('3', 'show_done_week', 'Done', show=True),
        Binding('q', 'quit', 'Quit', show=True),
        Binding('a', 'add_task', 'Add', show=True),
        Binding('question_mark', 'help', 'Help', show=True),
    ]

    def __init__(self, data_dir: Path, theme: str = 'textual-dark') -> None:
        super().__init__()
        self.data_dir = data_dir
        self._tasks: list[Task] = []
        self.theme = theme

    def on_mount(self) -> None:
        size = self.app.size
        if size.width < 100 or size.height < 30:
            self.exit(message='Terminal too small. Minimum size: 100×30.')
            return
        self._reload_tasks()
        self._show_view('kanban')

    def _reload_tasks(self) -> None:
        ensure_data_dir(self.data_dir)
        self._tasks = load_tasks(self.data_dir)

    def _show_view(self, view: str) -> None:
        from knbn.views.done_week import DoneByWeekView
        from knbn.views.kanban import KanbanView
        from knbn.views.tabular import TabularView

        container = self.query_one('#view-container')
        container.remove_children()
        if view == 'kanban':
            container.mount(KanbanView(self._tasks, self.data_dir))
        elif view == 'tabular':
            container.mount(TabularView(self._tasks, self.data_dir))
        elif view == 'done_week':
            container.mount(DoneByWeekView(self._tasks, self.data_dir))

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(id='view-container')
        yield Footer()

    def action_show_kanban(self) -> None:
        self._show_view('kanban')

    def action_show_tabular(self) -> None:
        self._show_view('tabular')

    def action_show_done_week(self) -> None:
        self._show_view('done_week')

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield SystemCommand('Theme', 'Change the current theme', self.action_change_theme)
        yield SystemCommand('Quit', 'Quit the application', self.action_quit)
        if screen.query('HelpPanel'):
            yield SystemCommand('Keys', 'Hide the keys panel', self.action_hide_help_panel)
        else:
            yield SystemCommand('Keys', 'Show help for the focused widget', self.action_show_help_panel)

    def action_add_task(self) -> None:
        from knbn.widgets.form import TaskForm

        self.push_screen(TaskForm(data_dir=self.data_dir, task=None))

    def action_help(self) -> None:
        from knbn.widgets.help import HelpOverlay

        self.push_screen(HelpOverlay())

    def on_task_form_task_saved(self) -> None:
        self._reload_tasks()
        self._show_view('kanban')

    def watch_theme(self, theme: str) -> None:
        from knbn.config import load_settings, save_settings

        if not hasattr(self, 'data_dir'):
            return
        settings = load_settings(self.data_dir)
        settings['theme'] = theme
        save_settings(self.data_dir, settings)
