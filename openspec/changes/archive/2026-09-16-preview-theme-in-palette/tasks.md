## 1. Preview and revert state

- [x] 1.1 Add `self._theme_preview_active: bool` and `self._theme_before_preview: str | None` instance attributes to `KnbnApp.__init__` in `src/knbn/app.py`, and verify `mypy` and existing tests still pass with the new attributes present.
- [x] 1.2 Override `action_change_theme` on `KnbnApp` to record `self._theme_before_preview = self.theme` before calling `self.search_themes()`, and verify by manually opening the theme palette (`Ctrl+P` → `Theme`) and confirming (via a temporary print/log or debugger) that the pre-palette theme is captured.

## 2. Live preview on highlight

- [x] 2.1 Add `on_command_palette_option_highlighted` handler on `KnbnApp` that resolves the highlighted option's prompt to a theme name via `self.available_themes` and, on a match, sets `self._theme_preview_active = True`, assigns `self.theme = <name>`, then clears the flag.
- [x] 2.2 Update `watch_theme` in `src/knbn/app.py` to skip the `load_settings`/`save_settings` persistence when `self._theme_preview_active` is `True`, and verify with a unit test that toggles the flag and asserts `settings.json` is not updated (`tests/test_app.py::test_theme_preview_flag_suppresses_persistence`).

## 3. Persist on confirm, revert on cancel

- [x] 3.1 Add `on_command_palette_closed` handler on `KnbnApp` that, when `event.option_selected` is `False` and `self._theme_before_preview` is set, sets the preview flag, restores `self.theme = self._theme_before_preview`, then clears both the flag and the stored value; when `option_selected` is `True`, explicitly persists `self.theme` via a shared `_persist_theme` helper (needed because the `ThemeProvider` selection callback re-assigns the same value already applied by preview, which Textual's reactive treats as a no-op and never routes through `watch_theme`).
- [x] 3.2 Verify with a unit test (using Textual's `Pilot`/`run_test`) that: opening the theme palette, highlighting a different theme, and confirming it updates both `self.theme` and `settings.json` (`tests/test_app.py::test_confirming_highlighted_theme_persists`).
- [x] 3.3 Verify with a unit test (using Textual's `Pilot`/`run_test`) that: opening the theme palette, highlighting a different theme, and pressing `Escape` restores `self.theme` to its original value and leaves `settings.json` unchanged (`tests/test_app.py::test_cancelling_palette_reverts_preview`).

## 4. Regression check

- [x] 4.1 Run `uv run pytest tests`, `uv run mypy src/`, and `uv run ruff check src/ tests/` and confirm all pass, since `app.py` is excluded from the coverage floor but must still type-check and lint cleanly.

## 5. Replace the command palette with a docked sidebar

The command-palette-based picker from section 1-4 covered most of the window. Replaced with a custom sidebar, per follow-up feedback.

- [x] 5.1 Add `src/knbn/widgets/theme_sidebar.py` with `ThemeSidebar(ModalScreen[None])`: a Textual `OptionList` of theme names docked to the right edge (`dock: right`, `width: 33%`, `min-width: 30`, `max-width: 60`), highlighting the current theme on mount and grabbing focus.
- [x] 5.2 Give `KnbnApp` public `preview_theme(theme)` / `confirm_theme(theme)` methods and have `ThemeSidebar` call them from `on_option_list_option_highlighted` / `on_option_list_option_selected`; `action_cancel` (bound to `Escape`) calls `preview_theme(original_theme)` to revert. Remove the now-unused `on_command_palette_option_highlighted` / `on_command_palette_closed` handlers, `_theme_before_preview`, and the `Command`/`CommandPalette` imports from `src/knbn/app.py`.
- [x] 5.3 Point `action_change_theme` at `self.push_screen(ThemeSidebar(self.theme))` instead of `self.search_themes()`.
- [x] 5.4 Verify the sidebar is actually bounded, not full-window, with a unit test asserting the mounted `OptionList`'s region width is less than the screen width and its x-offset is greater than 0 (`tests/test_app.py::test_theme_sidebar_docks_to_the_right_and_does_not_fill_the_window`).
- [x] 5.5 Verify the board stays visible behind the sidebar with a screenshot-based regression test (`app.export_screenshot()` before/after opening, checking for board text) (`tests/test_app.py::test_theme_sidebar_leaves_the_board_visible_behind_it`). This caught a real bug: `KnbnApp.CSS`'s bare `Screen { background: $surface; }` rule overrode `ThemeSidebar`'s own `background: transparent` (App-level CSS wins over widget `DEFAULT_CSS` regardless of selector specificity), painting the sidebar's screen fully opaque and hiding the board entirely. Fixed by adding a matching `ThemeSidebar { background: transparent; }` rule directly into `KnbnApp.CSS`.
- [x] 5.6 Update `tests/test_app.py`'s existing preview/confirm/cancel tests to exercise the sidebar (they already drove `action_change_theme` + `pilot.press('down'/'enter'/'escape')`, which needed no behavioral changes — only renamed for accuracy).
- [x] 5.7 Re-run `uv run pytest tests`, `uv run mypy src/`, `uv run ruff check src/ tests/`, and `uv run ruff format --check src/ tests/` and confirm all pass.
