"""Textual TUI application."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from textual.app import App, ComposeResult, SystemCommand
from textual.binding import Binding
from textual.events import Key
from textual.reactive import reactive
from textual.screen import Screen
from textual.timer import Timer
from textual.widgets import Footer, Static
from textual.widgets._footer import FooterKey

from knbn.config import (
    BoardConfig,
    BoardConfigError,
    build_default_board_config,
    load_board_config,
    load_settings,
    save_settings,
)
from knbn.model.store import ensure_data_dir, load_tasks
from knbn.model.task import Task
from knbn.widgets.search_bar import SearchBar

# Keys that are printable characters but should pass through to their action
# handlers in search mode rather than being typed into the search query.
_SEARCH_PASSTHROUGH_KEYS: frozenset[str] = frozenset({
    'question_mark',  # ? → action_help still fires; not added to query
})

_VIEW_ACTION = {
    'kanban': 'show_kanban',
    'tabular': 'show_tabular',
    'closed': 'show_closed',
}


class KnbnFooter(Footer):
    """Footer that highlights the active view tab key and shows the data dir."""

    active_view: reactive[str] = reactive('kanban')

    def __init__(self, data_dir: Path) -> None:
        super().__init__()
        home = Path.home()
        try:
            rel = data_dir.relative_to(home)
            self._data_dir_display = '~' if rel == Path() else f'~/{rel}'
        except ValueError:
            self._data_dir_display = str(data_dir)

    def compose(self) -> ComposeResult:
        yield from super().compose()
        yield Static(self._data_dir_display, id='data-dir-label')

    def bindings_changed(self, screen: Screen) -> None:
        super().bindings_changed(screen)
        self.call_after_refresh(self._apply_active_class)

    def watch_active_view(self) -> None:
        self.call_after_refresh(self._apply_active_class)

    def _apply_active_class(self) -> None:
        active_action = _VIEW_ACTION.get(self.active_view, '')
        for key_widget in self.query(FooterKey):
            key_widget.set_class(key_widget.action == active_action, '-active-tab')


class KnbnApp(App[None]):
    """Terminal Kanban board."""

    TITLE = 'knbn'
    CSS = """
    Screen {
        background: $surface;
    }
    ThemeSidebar {
        background: transparent;
    }
    #view-container {
        height: 1fr;
    }
    FooterKey.-active-tab .footer-key--key {
        color: $footer-key-background;
        background: $footer-key-foreground;
    }
    FooterKey.-active-tab .footer-key--description {
        color: $footer-key-foreground;
        background: $footer-description-background;
        text-style: bold;
    }
    #data-dir-label {
        width: 1fr;
        text-align: right;
        text-style: dim;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding('1', 'show_kanban', 'Kanban', show=True),
        Binding('2', 'show_tabular', 'Tabular', show=True),
        Binding('3', 'show_closed', 'Closed', show=True),
        Binding('q', 'quit', 'Quit', show=True),
        Binding('r', 'reload', 'Reload', show=True),
        Binding('a', 'add_task', 'Add', show=True),
        Binding('question_mark', 'help', 'Help', show=True),
        Binding('ctrl+f', 'toggle_search', 'Find', show=True),
    ]

    def __init__(self, data_dir: Path, theme: str = 'textual-dark') -> None:
        self.data_dir = data_dir
        super().__init__()
        self._tasks: list[Task] = []
        self._current_view: str = 'kanban'
        self._theme_preview_active = False
        self._preview_timer: Timer | None = None
        self.theme = theme
        self.board_config: BoardConfig = build_default_board_config()
        self._search_active: bool = False
        self._search_query: str = ''

    def on_mount(self) -> None:
        size = self.app.size
        if size.width < 100 or size.height < 30:
            self.exit(message='Terminal too small. Minimum size: 100×30.')
            return
        try:
            self.board_config = load_board_config(self.data_dir)
        except BoardConfigError as e:
            self.exit(message=f'Board config error: {e}')
            return
        self._reload_tasks()
        self._show_view('kanban')

    def _reload_tasks(self) -> None:
        ensure_data_dir(self.data_dir)
        self._tasks = load_tasks(self.data_dir)

    def _show_view(self, view: str) -> None:
        from knbn.views.done_week import ClosedView
        from knbn.views.kanban import KanbanView
        from knbn.views.tabular import TabularView

        self._reload_tasks()
        container = self.query_one('#view-container')
        container.remove_children()
        if view == 'kanban':
            container.mount(KanbanView(self._tasks, self.data_dir))
        elif view == 'tabular':
            container.mount(TabularView(self._tasks, self.data_dir))
        elif view == 'closed':
            container.mount(ClosedView(self._tasks, self.data_dir))
        self._current_view = view
        self.query_one(KnbnFooter).active_view = view

    def compose(self) -> ComposeResult:
        yield Static(id='view-container')
        yield SearchBar(id='search-bar')
        yield KnbnFooter(self.data_dir)

    async def _on_key(self, event: Key) -> None:
        if self._search_active and len(self.screen_stack) == 1:
            char = event.character
            if event.key == 'escape':
                self._deactivate_search()
                event.stop()
            elif event.key == 'backspace':
                if self._search_query:
                    self._search_query = self._search_query[:-1]
                    self._update_search_bar()
                    self._refilter_view()
                event.stop()
            elif (
                char is not None
                and char.isprintable()
                and event.key not in _SEARCH_PASSTHROUGH_KEYS
            ):
                self._search_query += char
                self._update_search_bar()
                self._refilter_view()
                event.stop()

    def action_toggle_search(self) -> None:
        if self._search_active:
            self._deactivate_search()
        else:
            self._activate_search()

    def _activate_search(self) -> None:
        self._search_active = True
        self._search_query = ''
        bar = self.query_one('#search-bar', SearchBar)
        bar.add_class('--active')
        self._update_search_bar()

    def _deactivate_search(self) -> None:
        self._search_active = False
        self._search_query = ''
        bar = self.query_one('#search-bar', SearchBar)
        bar.remove_class('--active')
        bar.update('')
        self._refilter_view()

    def _update_search_bar(self) -> None:
        text = f'/ {self._search_query}▇' if self._search_query else '/ ▇'
        self.query_one('#search-bar', SearchBar).update(text)

    def _refilter_view(self) -> None:
        container = self.query_one('#view-container')
        children = list(container.children)
        if children:
            self.call_after_refresh(children[0].recompose)

    def action_reload(self) -> None:
        if self._search_active:
            return
        self._show_view(self._current_view)

    def action_show_kanban(self) -> None:
        if self._search_active:
            return
        self._show_view('kanban')

    def action_show_tabular(self) -> None:
        if self._search_active:
            return
        self._show_view('tabular')

    def action_show_closed(self) -> None:
        if self._search_active:
            return
        self._show_view('closed')

    async def action_quit(self) -> None:
        if self._search_active:
            return
        self.exit()

    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield SystemCommand(
            'Theme', 'Change the current theme', self.action_change_theme
        )
        yield SystemCommand(
            'Category Colors',
            'Configure category colors',
            self.action_configure_category_colors,
        )
        if screen.query('HelpPanel'):
            yield SystemCommand(
                'Keys', 'Hide the keys panel', self.action_hide_help_panel
            )
        else:
            yield SystemCommand(
                'Keys', 'Show help for the focused widget', self.action_show_help_panel
            )

    def action_add_task(self) -> None:
        if self._search_active:
            return
        from knbn.views.kanban import KanbanView
        from knbn.widgets.form import TaskForm

        initial_status: str | None = None
        initial_priority: str | None = None
        if self._current_view == 'kanban':
            kanban_views = self.query(KanbanView)
            if kanban_views:
                ctx = kanban_views.first(KanbanView).get_lane_context()
                if ctx is not None:
                    initial_status, initial_priority = ctx

        self.push_screen(
            TaskForm(
                data_dir=self.data_dir,
                task=None,
                initial_status=initial_status,
                initial_priority=initial_priority,
            )
        )

    def action_help(self) -> None:
        from knbn.widgets.help import HelpOverlay

        self.push_screen(HelpOverlay())

    def action_change_theme(self) -> None:
        from knbn.widgets.theme_sidebar import ThemeSidebar

        self.push_screen(ThemeSidebar(self.theme))

    def action_configure_category_colors(self) -> None:
        from knbn.widgets.color_editor import CategoryColorEditor

        self.push_screen(
            CategoryColorEditor(data_dir=self.data_dir, board_config=self.board_config)
        )

    def preview_theme(self, theme: str) -> None:
        """Apply a theme live without persisting it to settings."""
        if self._preview_timer is not None:
            self._preview_timer.stop()
        self._preview_timer = self.set_timer(
            0.03, lambda: self._apply_preview_theme(theme)
        )

    def _apply_preview_theme(self, theme: str) -> None:
        self._theme_preview_active = True
        self.theme = theme
        self._theme_preview_active = False

    def confirm_theme(self, theme: str) -> None:
        """Apply a theme and persist it, replacing the previously saved value."""
        if self._preview_timer is not None:
            self._preview_timer.stop()
            self._preview_timer = None
        self._theme_preview_active = True  # prevent watch_theme from double-persisting
        self.theme = theme
        self._theme_preview_active = False
        self._persist_theme(theme)

    def on_task_form_task_saved(self) -> None:
        self._show_view(self._current_view)

    def on_category_color_editor_saved(self, event: object) -> None:
        from knbn.widgets.color_editor import CategoryColorEditor

        if isinstance(event, CategoryColorEditor.Saved):
            self.board_config = event.board_config
        self._show_view(self._current_view)

    def _persist_theme(self, theme: str) -> None:
        settings = load_settings(self.data_dir)
        settings['app']['theme'] = theme
        save_settings(self.data_dir, settings)

    def watch_theme(self, theme: str) -> None:
        if self._theme_preview_active:
            return
        self._persist_theme(theme)
