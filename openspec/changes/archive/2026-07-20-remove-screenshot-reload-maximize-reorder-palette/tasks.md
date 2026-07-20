## 1. Remove Reload binding and action

- [x] 1.1 In `src/knbn/app.py`, remove `Binding('r', 'reload', 'Reload', show=True)` from `BINDINGS`
- [x] 1.2 In `src/knbn/app.py`, remove the `action_reload` method

## 2. Override command palette system commands

- [x] 2.1 In `src/knbn/app.py`, add a `get_system_commands` override that yields `Theme → Quit → Keys` and omits Screenshot and Maximize/Minimize

## 3. Update help overlay

- [x] 3.1 In `src/knbn/widgets/help.py`, remove the `r  Reload from disk` line from `_HELP_TEXT`

## 4. Update canonical spec

- [x] 4.1 In `openspec/specs/tui-board/spec.md`, update the "Global quit" requirement to remove Reload and add the "Command palette" requirement
