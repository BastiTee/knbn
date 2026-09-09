## 1. Wire the key binding

- [x] 1.1 In `src/knbn/app.py`, add `Binding('r', 'reload', 'Reload', show=False)` to `KnbnApp.BINDINGS` and verify pressing `r` in the running TUI reloads the view without error

## 2. Update help overlay

- [x] 2.1 In `src/knbn/widgets/help.py`, add `  [cyan]r[/cyan]           Reload` to `_HELP_GLOBAL` (after the `?` line) and verify `?` displays `r  Reload` in the Global section

## 3. Update spec

- [x] 3.1 In `openspec/specs/tui-board/spec.md`, remove "There is no dedicated Reload keybinding." from the Global quit requirement and add the Global reload requirement (with scenarios) so the main spec matches the delta; verify `openspec validate` passes with no errors
