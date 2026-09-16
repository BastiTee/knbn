## Why

Quitting already has a dedicated, always-visible `q` binding shown in the footer toolbar, so listing `Quit` in the `Ctrl+P` command palette is redundant. Removing it shortens the palette to just the commands that have no simpler path (`Theme`, `Keys`).

## What Changes

- Remove the `Quit` entry from `KnbnApp.get_system_commands` in `src/knbn/app.py`. The palette will contain `Theme` then `Keys`.
- The `q` keybinding and footer `q Quit` button are unchanged; quitting via `q` or `Ctrl+C` continues to work exactly as before.

## Capabilities

### New Capabilities

<!-- None -->

### Modified Capabilities

- `tui-board`: The `Command palette` requirement no longer includes `Quit` among the exposed commands.

## Impact

- `src/knbn/app.py`: remove the `yield SystemCommand('Quit', 'Quit the application', self.action_quit)` line from `get_system_commands`.
- `openspec/specs/tui-board/spec.md`: update the `Command palette` requirement and its scenarios to drop `Quit`.
