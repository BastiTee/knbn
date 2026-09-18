## 1. Config persistence helper

- [x] 1.1 Add `save_board_config(data_dir: Path, board_config: BoardConfig) -> None` to `src/knbn/config.py` — serialises `BoardConfig` to a dict, loads current settings, replaces the `board` key, and calls `save_settings`. Verify with a unit test (`tests/test_config.py`) that `load_board_config()` returns the updated colors after a save round-trip.

## 2. Color picker overlay widget

- [x] 2.1 Create `src/knbn/widgets/color_editor.py` with `ColorPickerOverlay(ModalScreen[str | None])`. Include a 2×5 palette swatch grid (ten system palette colors from `board-config` spec), a live preview swatch, and a hex `Input` field. Confirm with `Enter` or a Confirm button; cancel with `Escape`. Verify by running the TUI and opening the overlay: clicking a swatch updates the hex input; typing a valid hex updates the preview; `Escape` returns `None`.

- [x] 2.2 Validate hex input on confirm: only accept `#[0-9a-f]{6}`. Show an inline error label and keep the overlay open on invalid input. Verify by entering `#ZZZ` and confirming — the overlay stays open with an error shown.

## 3. Category color editor screen

- [x] 3.1 Add `CategoryColorEditor(ModalScreen[None])` to `src/knbn/widgets/color_editor.py`. Compose a scrollable list of category rows (name + swatch + hex value), Save and Cancel buttons, and define `BINDINGS = [Binding('ctrl+s', 'save', 'Save'), Binding('escape', 'cancel', 'Cancel')]`. Seed an internal `_pending: dict[str, str]` from the passed `BoardConfig` on mount. Verify the screen opens and all categories are listed by launching the palette command.

- [x] 3.2 Wire row selection: pressing `Enter` or clicking a category row pushes `ColorPickerOverlay`. On a non-`None` return, update `_pending` for that category and re-render the row's swatch and hex label. Verify by selecting a category and changing its color — the row updates immediately without closing the editor.

- [x] 3.3 Show a dirty indicator in the screen title or a status line whenever `_pending` differs from the original colors. Verify that the indicator appears after one color change and disappears after cancel/reopen.

- [x] 3.4 Implement `action_save`: call `save_board_config(data_dir, updated_board_config)`, post `CategoryColorEditor.Saved(board_config)`, and dismiss. Implement `action_cancel`: dismiss without saving. Verify that `settings.json` is unchanged after cancel, and updated after save.

## 4. App integration

- [x] 4.1 Add `CategoryColorEditor.Saved` message class (carries `board_config: BoardConfig`) inside `color_editor.py`. Handle it in `KnbnApp.on_category_color_editor_saved`: update `self.board_config` and call `self.call_after_refresh(self.recompose)` to refresh the running TUI. Verify that category colors change on the board immediately after saving without a restart.

- [x] 4.2 Add a `"Configure Category Colors"` entry to `KnbnApp.get_system_commands` that calls `self.push_screen(CategoryColorEditor(data_dir=self.data_dir, board_config=self.board_config))`. Verify the command appears in `Ctrl+P` and opens the editor.

## 5. Tests

- [x] 5.1 Extend `tests/test_config.py` with tests covering `save_board_config`

- [x] 5.2 Run `make build` (full chain: tests + mypy + lint + format) and confirm it passes with no new errors or type violations.
