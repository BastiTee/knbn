## Context

`TaskForm` is a `ModalScreen` subclass. It already has `Binding('escape', 'cancel', 'Cancel')` and a `_save()` method. Adding `Ctrl+S` is a straightforward binding addition with no architectural decisions required. `Ctrl+C` is intentionally excluded — it conflicts with Textual's app-level quit handler and `Esc` already serves as the cancel shortcut.

## Goals / Non-Goals

**Goals:**
- `Ctrl+S` triggers save when title has ≥1 non-whitespace character (reuses existing `_save()` guard)

**Non-Goals:**
- Adding a `Ctrl+C` cancel shortcut (conflicts with quit handler; `Esc` covers this)
- Changing the save validation logic
- Adding shortcuts to any other modal (detail panel, confirm dialogs, etc.)

## Decisions

### `action_save` vs reusing `_save` directly

`action_save` simply calls `self._save()` — no duplication needed.
