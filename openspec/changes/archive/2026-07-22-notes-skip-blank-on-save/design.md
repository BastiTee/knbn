## Context

`open_notes_in_editor` in `store.py` creates an empty file before launching the editor so the editor has a path to open. When the user exits without writing anything, that empty (or whitespace-only) file persists. The notes-presence check (`notes_exist`) then returns `True` for that task and the card shows a spurious `[N]` indicator.

The fix is entirely within `open_notes_in_editor` — no other layer needs to change.

## Goals / Non-Goals

**Goals:**
- Delete a newly created notes file when the editor exits and the file contains only whitespace (or is 0 bytes)
- Leave pre-existing notes files untouched regardless of their content after editing

**Non-Goals:**
- Prompting the user before deletion
- Handling the case where an existing file is cleared to blank (preserve existing files as-is)
- Any changes to slug logic, CSV schema, or TUI layer

## Decisions

### Track whether the file was pre-existing before the editor opens

Record `already_existed = notes_path.exists()` before creating the empty file. After the editor returns, check content only when `not already_existed`. This avoids accidentally deleting a file the user intentionally cleared.

**Alternatives considered:**
- Check content unconditionally — rejected because it would delete an existing file that a user intentionally emptied.
- Use a temp file and only move it into place if non-blank — more complex, and requires the editor to be given a temp path rather than the final path, which breaks editor history/plugins that key on filename.

### Strip and check, then unlink

After the editor exits, read the file and call `.strip()`. If the result is empty, `unlink()` the file. This handles all whitespace variants (spaces, tabs, newlines, `\r\n`).

## Risks / Trade-offs

- [Risk] A user writes a single space intentionally as a placeholder → Mitigation: Acceptable loss; the spec requires at least one non-whitespace character. A space-only file has no meaningful content.
- [Risk] Editor writes metadata or BOM bytes → Mitigation: `.strip()` on decoded text covers common cases; BOM-only files are exotic and not a practical concern for a personal tool.

## Migration Plan

No migration required. Existing non-empty notes files are unaffected. Empty files that already exist will remain (only newly created blank files are cleaned up).
