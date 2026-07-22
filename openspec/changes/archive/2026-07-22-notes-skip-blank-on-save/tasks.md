## 1. Core Implementation

- [x] 1.1 In `open_notes_in_editor` (`store.py`), record `already_existed = notes_path.exists()` before creating the empty file
- [x] 1.2 After `subprocess.run`, if `not already_existed` and the file exists, read its content and delete it if `.strip()` is empty

## 2. Tests

- [x] 2.1 Add test: editor exits with empty file → file is deleted
- [x] 2.2 Add test: editor exits with whitespace-only content → file is deleted
- [x] 2.3 Add test: editor exits with non-whitespace content → file is kept
- [x] 2.4 Add test: pre-existing file cleared to blank → file is preserved

## 3. Spec Sync

- [x] 3.1 Update `openspec/specs/task-notes/spec.md` with the new "Discard newly created blank notes file" and "Preserve existing file cleared to blank" scenarios
