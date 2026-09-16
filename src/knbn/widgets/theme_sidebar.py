"""Theme picker sidebar, docked to the right edge like the keys help panel."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import OptionList
from textual.widgets.option_list import Option


class ThemeSidebar(ModalScreen[None]):
    """Browse themes in a sidebar, previewing each as it is highlighted."""

    BINDINGS = [
        Binding('escape', 'cancel', 'Cancel'),
    ]

    DEFAULT_CSS = """
    ThemeSidebar {
        background: transparent;
    }
    ThemeSidebar > OptionList {
        dock: right;
        width: 33%;
        min-width: 30;
        max-width: 60;
        height: 1fr;
        border-left: vkey $foreground 30%;
        background: $surface;
        padding: 0 1;
    }
    """

    def __init__(self, current_theme: str) -> None:
        super().__init__()
        self._original_theme = current_theme

    def compose(self) -> ComposeResult:
        theme_names = sorted(self.app.available_themes)
        yield OptionList(*(Option(name, id=name) for name in theme_names))

    def on_mount(self) -> None:
        option_list = self.query_one(OptionList)
        theme_names = sorted(self.app.available_themes)
        try:
            option_list.highlighted = theme_names.index(self._original_theme)
        except ValueError:
            option_list.highlighted = 0
        option_list.focus()

    def on_option_list_option_highlighted(
        self, event: OptionList.OptionHighlighted
    ) -> None:
        if event.option_id is not None:
            self.app.preview_theme(event.option_id)  # type: ignore[attr-defined]

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option_id is not None:
            self.app.confirm_theme(event.option_id)  # type: ignore[attr-defined]
        self.dismiss(None)

    def action_cancel(self) -> None:
        self.app.preview_theme(self._original_theme)  # type: ignore[attr-defined]
        self.dismiss(None)
