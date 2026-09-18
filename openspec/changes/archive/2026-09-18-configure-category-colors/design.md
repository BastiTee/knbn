## Context

`BoardConfig` already holds `categories: list[CategoryConfig]` where each entry has `name` and `color` (validated 6-digit hex). `save_settings()` in `config.py` provides atomic JSON persistence. The command palette is gated through `get_system_commands` in `app.py`. `TaskForm` establishes the save/cancel modal pattern (`Ctrl+S` / `Escape`, `TaskSaved` message, `push_screen`).

See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Category color editor reachable from the `Ctrl+P` palette with save/cancel UX matching `TaskForm`.
- Terminal-native color picker: palette swatches for the ten system colors + hex input override.
- `save_board_config()` helper that atomically updates only the `board.categories` block.
- Board reloads (color tokens refresh) after save, without restarting the TUI.

**Non-Goals:**
- Full RGB/HSL slider color picker.
- Adding/removing/renaming categories (a separate workflow).
- Editing other board config fields (statuses, priorities, etc.).
- Live preview of category colors on the board while the editor is open.

## Decisions

### Color picker widget: palette grid + hex input, no sliders

A 2×5 swatch grid of the ten palette colors plus a hex text field covers the common cases (pick a predefined color, or type an exact hex) without needing complex slider math in a terminal. This is consistent with the terminal-native aesthetic and avoids importing a color-space library.

_Alternative considered_: Full HSL sliders using Textual's `Slider` widget — rejected because the required precision (360 hue values) maps poorly to keyboard navigation and adds significant implementation complexity for minimal user benefit.

### Both screens in one file: `src/knbn/widgets/color_editor.py`

`ColorPickerOverlay` is only ever used by `CategoryColorEditor`. Keeping them in a single module avoids a proliferation of tiny files. Follows the pattern of `form.py` hosting both `DueInput` and `TaskForm`.

### Reload via `CategoryColorEditor.Saved` message carrying new `BoardConfig`

The editor posts a `CategoryColorEditor.Saved(board_config)` message on save. `KnbnApp` handles it by updating `self.board_config` and calling `self.call_after_refresh(self.recompose)` (async-safe from sync context). This avoids re-reading disk inside the app and keeps the flow synchronous from the app's perspective.

_Alternative considered_: Reload from disk after dismissal — rejected because it requires the app to know which screen just saved and introduces a race if the dismiss callback runs before the save completes.

### Dirty state: local mutable dict, not reactive attributes

`CategoryColorEditor` keeps a `dict[str, str]` (category name → pending hex) that is seeded from `BoardConfig` on open. Changes go into this dict only; nothing is written until `action_save`. This mirrors how `TaskForm` accumulates edits locally before posting `TaskSaved`.

### `save_board_config()` wraps `load_settings` + `save_settings`

Rather than introducing a new persistence path, `save_board_config(data_dir, board_config)` loads the full settings dict, replaces `settings["board"]` with the serialised `BoardConfig`, and calls `save_settings`. This reuses the existing atomic write path and preserves the `app` block.

## Risks / Trade-offs

- **Swatch color rendering depends on terminal color support**: Textual renders colored backgrounds via ANSI; terminals with limited color depth will approximate. This is inherent to terminal UIs and does not affect correctness.
- **Nested modal depth**: `CategoryColorEditor` pushes `ColorPickerOverlay` on top of itself. Textual supports nested `push_screen` calls, but `Escape` semantics must be handled carefully — the overlay's `Escape` must dismiss only the overlay, not the editor behind it. Both screens declare their own `BINDINGS` and `action_dismiss`, so this is manageable.
- **Board recompose on save**: `recompose()` is async in Textual 8 and must be called with `call_after_refresh`. A missed `await` or direct sync call will silently fail. The CLAUDE.md already documents this constraint.

## Migration Plan

No data migration required. `save_board_config` writes the same `settings.json` format the existing `load_board_config` reads. Existing installs with no `settings.json` are unaffected (the editor initialises from the loaded `BoardConfig`, which defaults gracefully).
