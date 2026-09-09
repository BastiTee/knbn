## Context

`action_reload` already exists in `app.py` (calls `_show_view(self._current_view)` which re-reads the CSV and remounts the view). It is not exposed via any key binding. The `r` key is currently unbound globally.

See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Expose `action_reload` via the `r` key globally
- Surface `r Reload` in the help overlay

**Non-Goals:**
- Auto-reload / file-watch (no inotify/polling)
- Preserving cursor position after reload (view remounts from scratch, same as switching views)

## Decisions

**Wire `r` directly to existing `action_reload`** — the method already does the right thing: reloads tasks from disk and remounts the current view. No new logic needed.

Alternative considered: add a separate reload path that preserves focus. Rejected — view remount on view switch already discards focus and users accept this; adding focus preservation would be disproportionate scope.

**Add `r Reload` to the help overlay `_HELP_GLOBAL` string** — all global keys are listed there. `show=False` on the Binding keeps the footer uncluttered (footer already has 6 entries).

## Risks / Trade-offs

- [Remount discards focus] → Acceptable; same behaviour as pressing `1`/`2`/`3` to re-enter the current view. Users pressing `r` expect a refresh, not a no-op.
- [Key conflict] → `r` is unbound in all three views and in the app's global scope; no conflict.
