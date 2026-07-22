## Why

When a user opens notes for a task and exits the editor without typing anything, a 0-byte or whitespace-only file is left behind. This causes spurious notes indicators on task cards and pollutes the notes directory with empty files.

## What Changes

- After the editor exits, check if the notes file contains at least one non-whitespace character
- If the file is empty or whitespace-only and it was newly created (did not exist before), delete it
- If the file is empty or whitespace-only and it already existed, leave it unchanged (preserve existing content)

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `task-notes`: Add a post-save guard — a newly created notes file is deleted if it contains no non-whitespace content after the editor closes

## Impact

- `src/knbn/model/store.py`: `open_notes_in_editor` — add post-editor blank-check and conditional delete
- No changes to CSV schema, slug logic, or TUI layer
