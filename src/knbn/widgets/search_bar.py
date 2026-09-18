"""Search bar widget displayed above the footer when search is active."""

from __future__ import annotations

from textual.widgets import Static


class SearchBar(Static):
    """Displays the active search query; keyboard input handled by KnbnApp._on_key."""

    DEFAULT_CSS = """
    SearchBar {
        height: 1;
        display: none;
        background: $primary-darken-2;
        color: $text;
        padding: 0 1;
    }
    SearchBar.--active {
        display: block;
    }
    """

    def __init__(self, **kwargs: object) -> None:
        super().__init__('', **kwargs)  # type: ignore[arg-type]
