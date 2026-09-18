"""Mixin for widgets and views that need typed access to KnbnApp state."""

from __future__ import annotations

from knbn.config import BoardConfig


class KnbnWidgetMixin:
    """Single point of access to KnbnApp attributes from any widget or view.

    All properties use type: ignore because self.app is typed as App[Any]
    by Textual and does not expose KnbnApp-specific attributes statically.
    """

    @property
    def _board_config(self) -> BoardConfig:
        return self.app.board_config  # type: ignore[attr-defined,no-any-return]

    @property
    def _search_query(self) -> str:
        return self.app._search_query  # type: ignore[attr-defined,no-any-return]

    @property
    def _search_active(self) -> bool:
        return self.app._search_active  # type: ignore[attr-defined,no-any-return]
