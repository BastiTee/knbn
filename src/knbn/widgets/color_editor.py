"""Category color editor and color picker overlay."""

from __future__ import annotations

import re
from dataclasses import replace
from pathlib import Path

from rich.text import Text
from textual.app import ComposeResult
from textual.binding import Binding
from textual.color import Color
from textual.containers import Horizontal, Vertical
from textual.events import Click, Key
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Input, ListItem, ListView, Static

from knbn.config import (
    CATEGORY_COLOR_PALETTE,
    BoardConfig,
    CategoryConfig,
    save_board_config,
)

_HEX_RE = re.compile(r'^#[0-9a-f]{6}$')

_PALETTE = CATEGORY_COLOR_PALETTE

_PALETTE_COLS = 5
_PALETTE_CELL_W = 4  # chars per cell

# 10 qualitative schemes x 10 hex colors each.
# Sources: seaborn palettes.py (Deep/Muted/Pastel/Bright/Colorblind/Dark),
#          matplotlib tab10, ColorBrewer Paired, Paul Tol Muted (2012),
#          CSS named earth-tone colors.
_SCHEMES: dict[str, list[str]] = {
    'Tab10': [
        '#1f77b4',
        '#ff7f0e',
        '#2ca02c',
        '#d62728',
        '#9467bd',
        '#8c564b',
        '#e377c2',
        '#7f7f7f',
        '#bcbd22',
        '#17becf',
    ],
    'Deep': [
        '#4c72b0',
        '#dd8452',
        '#55a868',
        '#c44e52',
        '#8172b3',
        '#937860',
        '#da8bc3',
        '#8c8c8c',
        '#ccb974',
        '#64b5cd',
    ],
    'Muted': [
        '#4878d0',
        '#ee854a',
        '#6acc64',
        '#d65f5f',
        '#956cb4',
        '#8c613c',
        '#dc7ec0',
        '#797979',
        '#d5bb67',
        '#82c6e2',
    ],
    'Pastel': [
        '#a1c9f4',
        '#ffb482',
        '#8de5a1',
        '#ff9f9b',
        '#d0bbff',
        '#debb9b',
        '#fab0e4',
        '#cfcfcf',
        '#fffea3',
        '#b9f2f0',
    ],
    'Bright': [
        '#023eff',
        '#ff7c00',
        '#1ac938',
        '#e8000b',
        '#8b2be2',
        '#9f4800',
        '#f14cc1',
        '#a3a3a3',
        '#ffc400',
        '#00d7ff',
    ],
    'Colorblind': [
        '#0173b2',
        '#de8f05',
        '#029e73',
        '#d55e00',
        '#cc78bc',
        '#ca9161',
        '#fbafe4',
        '#949494',
        '#ece133',
        '#56b4e9',
    ],
    'Dark': [
        '#001c7f',
        '#b1400d',
        '#12711c',
        '#8c0800',
        '#591e71',
        '#592f0d',
        '#a23582',
        '#3c3c3c',
        '#b8850a',
        '#006374',
    ],
    'Paired': [
        '#a6cee3',
        '#1f78b4',
        '#b2df8a',
        '#33a02c',
        '#fb9a99',
        '#e31a1c',
        '#fdbf6f',
        '#ff7f00',
        '#cab2d6',
        '#6a3d9a',
    ],
    'Tol Muted': [
        '#332288',
        '#117733',
        '#44aa99',
        '#88ccee',
        '#ddcc77',
        '#cc6677',
        '#aa4499',
        '#882255',
        '#999933',
        '#661100',
    ],
    'Earth': [
        '#8b4513',
        '#cd853f',
        '#daa520',
        '#a0522d',
        '#bc8f8f',
        '#556b2f',
        '#5f9ea0',
        '#f4a460',
        '#bdb76b',
        '#6b8e23',
    ],
}


class PaletteGrid(Static, can_focus=True):
    """Focusable 2×5 palette grid — arrow keys + Enter or click to pick."""

    class Highlighted(Message):
        """Posted when the cursor moves over a colour (preview, no commit)."""

        def __init__(self, color: str) -> None:
            super().__init__()
            self.color = color

    class Selected(Message):
        """Posted when the user commits to a colour (Enter or click)."""

        def __init__(self, color: str) -> None:
            super().__init__()
            self.color = color

    DEFAULT_CSS = """
    PaletteGrid {
        width: 20;
        height: 2;
    }
    PaletteGrid:focus {
        border: none;
    }
    """

    def __init__(self, initial_color: str | None = None, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._cursor = (
            _PALETTE.index(initial_color)
            if initial_color and initial_color in _PALETTE
            else 0
        )

    def render(self) -> Text:
        t = Text(no_wrap=True)
        for row in range(2):
            for col in range(_PALETTE_COLS):
                idx = row * _PALETTE_COLS + col
                color = _PALETTE[idx]
                # ">  <" marks the keyboard cursor; "    " for all other cells
                cell = '>  <' if idx == self._cursor else '    '
                t.append(cell, style=f'bold on {color}')
            if row == 0:
                t.append('\n')
        return t

    async def _on_key(self, event: Key) -> None:
        if event.key == 'left':
            event.stop()
            self._cursor = (self._cursor - 1) % len(_PALETTE)
            self.refresh()
            self.post_message(PaletteGrid.Highlighted(_PALETTE[self._cursor]))
        elif event.key == 'right':
            event.stop()
            self._cursor = (self._cursor + 1) % len(_PALETTE)
            self.refresh()
            self.post_message(PaletteGrid.Highlighted(_PALETTE[self._cursor]))
        elif event.key == 'up':
            event.stop()
            new = self._cursor - _PALETTE_COLS
            if new >= 0:
                self._cursor = new
                self.refresh()
                self.post_message(PaletteGrid.Highlighted(_PALETTE[self._cursor]))
        elif event.key == 'down':
            event.stop()
            new = self._cursor + _PALETTE_COLS
            if new < len(_PALETTE):
                self._cursor = new
                self.refresh()
                self.post_message(PaletteGrid.Highlighted(_PALETTE[self._cursor]))
        elif event.key == 'enter':
            event.stop()
            self.post_message(PaletteGrid.Selected(_PALETTE[self._cursor]))

    def on_click(self, event: Click) -> None:
        col = event.x // _PALETTE_CELL_W
        row = event.y
        if 0 <= col < _PALETTE_COLS and 0 <= row < 2:
            idx = row * _PALETTE_COLS + col
            self._cursor = idx
            self.refresh()
            self.post_message(PaletteGrid.Selected(_PALETTE[idx]))


class CategoryRow(Horizontal):
    """A row displaying category name, color swatch, and hex value."""

    def __init__(self, name: str, color: str) -> None:
        super().__init__()
        self._cat_name = name
        self._cat_color = color

    def compose(self) -> ComposeResult:
        yield Static(self._cat_name, classes='row-name')
        yield Static(' ', classes='row-swatch')
        yield Static(self._cat_color, classes='row-hex')

    def on_mount(self) -> None:
        self.query_one('.row-swatch', Static).styles.background = Color.parse(
            self._cat_color
        )

    def update_color(self, color: str) -> None:
        self._cat_color = color
        self.query_one('.row-swatch', Static).styles.background = Color.parse(color)
        self.query_one('.row-hex', Static).update(color)


class ColorPickerOverlay(ModalScreen[str | None]):
    """Modal overlay for picking a hex color from a palette or typing one."""

    BINDINGS = [
        Binding('escape', 'cancel', 'Cancel', show=True),
        Binding('ctrl+s', 'confirm_pick', 'Confirm', show=True),
    ]

    DEFAULT_CSS = """
    ColorPickerOverlay {
        align: center middle;
    }
    ColorPickerOverlay > Vertical {
        background: $surface;
        border: round $primary;
        padding: 1 2;
        width: 46;
        height: auto;
    }
    ColorPickerOverlay .picker-title {
        text-style: bold;
        margin-bottom: 0;
    }
    ColorPickerOverlay .picker-hint {
        color: $text-muted;
        margin-bottom: 1;
    }
    ColorPickerOverlay #palette-grid {
        margin-bottom: 1;
    }
    ColorPickerOverlay #preview-row {
        height: 2;
        margin-top: 1;
        align: left middle;
    }
    ColorPickerOverlay #preview-label {
        width: auto;
        margin-right: 1;
        content-align: left middle;
    }
    ColorPickerOverlay #preview-swatch {
        width: 8;
        height: 2;
    }
    ColorPickerOverlay #picker-error {
        color: $error;
        height: 1;
        margin-top: 0;
    }
    ColorPickerOverlay #picker-buttons {
        margin-top: 1;
        height: 3;
    }
    """

    def __init__(self, current_color: str) -> None:
        super().__init__()
        self._current_color = current_color

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static('Pick Color', classes='picker-title')
            yield Static(
                '↑↓←→ navigate  Enter/click select  Tab for custom hex',
                classes='picker-hint',
            )
            yield PaletteGrid(initial_color=self._current_color, id='palette-grid')
            with Horizontal(id='preview-row'):
                yield Static('Preview:', id='preview-label')
                yield Static(' ', id='preview-swatch')
            yield Input(
                value=self._current_color,
                placeholder='#rrggbb',
                id='hex-input',
            )
            yield Static('', id='picker-error')
            with Horizontal(id='picker-buttons'):
                yield Button('Confirm hex', id='confirm-btn', variant='primary')
                yield Button('Cancel', id='cancel-btn')

    def on_mount(self) -> None:
        self._update_preview(self._current_color)
        self.query_one('#palette-grid', PaletteGrid).focus()

    def _update_preview(self, hex_color: str) -> None:
        if _HEX_RE.match(hex_color):
            self.query_one('#preview-swatch', Static).styles.background = Color.parse(
                hex_color
            )

    def on_palette_grid_highlighted(self, event: PaletteGrid.Highlighted) -> None:
        self._update_preview(event.color)

    def on_palette_grid_selected(self, event: PaletteGrid.Selected) -> None:
        self.dismiss(event.color)

    def on_input_changed(self, event: Input.Changed) -> None:
        self._update_preview(event.value)
        self.query_one('#picker-error', Static).update('')

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.action_confirm_pick()

    def action_confirm_pick(self) -> None:
        hex_val = self.query_one('#hex-input', Input).value.strip()
        if not _HEX_RE.match(hex_val):
            self.query_one('#picker-error', Static).update(
                f'Must be #rrggbb (got {hex_val!r})'
            )
            return
        self.dismiss(hex_val)

    def action_cancel(self) -> None:
        self.dismiss(None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'confirm-btn':
            self.action_confirm_pick()
        elif event.button.id == 'cancel-btn':
            self.action_cancel()


class SchemeSwatchBar(Static):
    """Read-only 1×10 swatch strip for scheme preview rows."""

    DEFAULT_CSS = """
    SchemeSwatchBar {
        width: 20;
        height: 1;
    }
    """

    def __init__(self, colors: list[str]) -> None:
        super().__init__('')
        self._colors = colors

    def render(self) -> Text:
        t = Text(no_wrap=True)
        for color in self._colors:
            t.append('  ', style=f'on {color}')
        return t


class SchemeRow(Horizontal):
    """A row showing a scheme name and its colour swatch strip."""

    def __init__(self, name: str, colors: list[str]) -> None:
        super().__init__()
        self._scheme_name = name
        self._colors = colors

    def compose(self) -> ComposeResult:
        yield Static(self._scheme_name, classes='scheme-name')
        yield SchemeSwatchBar(self._colors)


class SchemePickerOverlay(ModalScreen[list[str] | None]):
    """Modal for selecting a colour scheme to apply to all categories."""

    BINDINGS = [
        Binding('escape', 'cancel', 'Cancel', show=True),
    ]

    DEFAULT_CSS = """
    SchemePickerOverlay {
        align: center middle;
    }
    SchemePickerOverlay > Vertical {
        background: $surface;
        border: round $primary;
        padding: 1 2;
        width: 40;
        height: auto;
        max-height: 22;
    }
    SchemePickerOverlay .scheme-title {
        text-style: bold;
        margin-bottom: 0;
    }
    SchemePickerOverlay .scheme-hint {
        color: $text-muted;
        margin-bottom: 1;
    }
    SchemePickerOverlay #scheme-list {
        height: auto;
        max-height: 12;
    }
    SchemePickerOverlay ListItem.-highlight SchemeRow {
        background: $accent 20%;
    }
    SchemePickerOverlay SchemeRow {
        height: 1;
        align: left middle;
    }
    SchemePickerOverlay .scheme-name {
        width: 12;
    }
    SchemePickerOverlay #scheme-buttons {
        margin-top: 1;
        height: 3;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static('Color Schemes', classes='scheme-title')
            yield Static('↑↓ navigate  Enter/click to apply', classes='scheme-hint')
            yield ListView(
                *[
                    ListItem(SchemeRow(name, colors), id=f'scheme-{i}')
                    for i, (name, colors) in enumerate(_SCHEMES.items())
                ],
                id='scheme-list',
            )
            with Horizontal(id='scheme-buttons'):
                yield Button('Cancel', id='cancel-btn')

    def on_mount(self) -> None:
        self.query_one('#scheme-list', ListView).focus()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        self.dismiss(list(_SCHEMES.values())[event.index])

    def action_cancel(self) -> None:
        self.dismiss(None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'cancel-btn':
            self.action_cancel()


class CategoryColorEditor(ModalScreen[None]):
    """Modal screen for viewing and editing category colors."""

    class Saved(Message):
        """Posted when the user saves the updated category colors."""

        def __init__(self, board_config: BoardConfig) -> None:
            super().__init__()
            self.board_config = board_config

    BINDINGS = [
        Binding('ctrl+s', 'save', 'Save', show=True),
        Binding('ctrl+t', 'apply_scheme', 'Scheme', show=True),
        Binding('escape', 'cancel', 'Cancel', show=True),
    ]

    DEFAULT_CSS = """
    CategoryColorEditor {
        align: center middle;
    }
    CategoryColorEditor > Vertical {
        background: $surface;
        border: round $primary;
        padding: 1 2;
        width: 52;
        height: auto;
        max-height: 30;
    }
    CategoryColorEditor .editor-title {
        text-style: bold;
        margin-bottom: 0;
    }
    CategoryColorEditor .editor-hint {
        color: $text-muted;
        margin-bottom: 1;
    }
    CategoryColorEditor #category-list {
        height: auto;
        max-height: 14;
    }
    CategoryColorEditor ListItem.-highlight CategoryRow {
        background: $accent 20%;
    }
    CategoryColorEditor CategoryRow {
        height: 1;
        align: left middle;
    }
    CategoryColorEditor .row-name {
        width: 1fr;
    }
    CategoryColorEditor .row-swatch {
        width: 4;
        height: 1;
    }
    CategoryColorEditor .row-hex {
        width: 8;
        margin-left: 1;
    }
    CategoryColorEditor #dirty-indicator {
        height: 1;
        color: $warning;
        margin-top: 1;
    }
    CategoryColorEditor #editor-buttons {
        margin-top: 1;
        height: 3;
    }
    """

    def __init__(self, data_dir: Path, board_config: BoardConfig) -> None:
        super().__init__()
        self._data_dir = data_dir
        self._board_config = board_config
        self._original: dict[str, str] = {
            c.name: c.color for c in board_config.categories
        }
        self._pending: dict[str, str] = dict(self._original)

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static('Category Colors', classes='editor-title')
            yield Static(
                '↑↓ navigate  Enter/click edit  Ctrl+T scheme', classes='editor-hint'
            )
            yield ListView(
                *[
                    ListItem(
                        CategoryRow(c.name, c.color),
                        id=f'cat-{i}',
                    )
                    for i, c in enumerate(self._board_config.categories)
                ],
                id='category-list',
            )
            yield Static('', id='dirty-indicator')
            with Horizontal(id='editor-buttons'):
                yield Button('Save', id='save-btn', variant='primary')
                yield Button('Scheme', id='scheme-btn')
                yield Button('Cancel', id='cancel-btn')

    def on_mount(self) -> None:
        self.query_one('#category-list', ListView).focus()

    def _refresh_dirty(self) -> None:
        dirty = any(self._pending[k] != self._original[k] for k in self._original)
        self.query_one('#dirty-indicator', Static).update(
            '* unsaved changes' if dirty else ''
        )

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        idx = event.index
        cat = self._board_config.categories[idx]
        current_color = self._pending[cat.name]
        list_item = event.item

        def _on_color_picked(color: str | None) -> None:
            if color is not None:
                self._pending[cat.name] = color
                list_item.query_one(CategoryRow).update_color(color)
                self._refresh_dirty()

        self.app.push_screen(ColorPickerOverlay(current_color), _on_color_picked)

    def action_apply_scheme(self) -> None:
        def _on_scheme_picked(colors: list[str] | None) -> None:
            if colors is None:
                return
            for i, cat in enumerate(self._board_config.categories):
                if i < len(colors):
                    self._pending[cat.name] = colors[i]
            lv = self.query_one('#category-list', ListView)
            for i, item in enumerate(lv.query(ListItem)):
                if i < len(colors):
                    item.query_one(CategoryRow).update_color(colors[i])
            self._refresh_dirty()

        self.app.push_screen(SchemePickerOverlay(), _on_scheme_picked)

    def action_save(self) -> None:
        updated_categories = [
            CategoryConfig(name=c.name, color=self._pending[c.name])
            for c in self._board_config.categories
        ]
        updated_config = replace(self._board_config, categories=updated_categories)
        save_board_config(self._data_dir, updated_config)
        self.post_message(CategoryColorEditor.Saved(updated_config))
        self.dismiss()

    def action_cancel(self) -> None:
        self.dismiss()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'save-btn':
            self.action_save()
        elif event.button.id == 'scheme-btn':
            self.action_apply_scheme()
        elif event.button.id == 'cancel-btn':
            self.action_cancel()
