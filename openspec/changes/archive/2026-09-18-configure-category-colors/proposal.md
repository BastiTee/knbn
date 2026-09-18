## Why

Users have category colors in their board config but no in-app way to inspect or change them — doing so requires manually editing `settings.json`. Adding a color editor to the command palette closes this gap and makes color configuration a first-class TUI feature.

## What Changes

- Adds a **Category Color Editor** screen reachable from the `Ctrl+P` command palette.
- The screen lists all configured categories alongside their current color swatches.
- Selecting a category opens a terminal color picker modal where the user can choose a new color.
- `Ctrl+S` or a **Save** button persists the updated colors to `settings.json` and reloads the board config; `Escape` discards all pending changes.
- The save/abort UX mirrors the Task Editor (`TaskForm`): `Ctrl+S` saves, `Escape` cancels without writing.

## Capabilities

### New Capabilities

- `category-color-editor`: TUI modal screen for viewing and interactively editing category colors, accessible from the command palette.

### Modified Capabilities

- `board-config`: `save_board_config()` helper must be available (or introduced) to write the updated `board.categories` list back to `settings.json` atomically.

## Impact

- **`src/knbn/app.py`** — add `"Configure Category Colors"` entry to `get_system_commands`; handle `CategoryColorEditor.Saved` message to reload board config and refresh views.
- **`src/knbn/config.py`** — add `save_board_config()` (writes the updated `BoardConfig` back into `settings.json` under the `board` key, atomically).
- **`src/knbn/widgets/color_editor.py`** (new) — `CategoryColorEditor` modal screen with category list, inline color swatch preview, embedded color picker, Save/Cancel buttons, and `Ctrl+S` binding.
- No changes to CSV schema, task model, or store.
