# task-notes

## Purpose

Per-task Markdown notes files, editor integration, and card indicators.

## Requirements

### Requirement: Notes file creation and editing
The system SHALL allow creating and editing a per-task Markdown notes file via the TUI (key `n` on a focused card or in the detail panel) or via `knbn add`. The file SHALL be opened in the editor specified by `$EDITOR`, falling back to `nano` if unset.

#### Scenario: Open notes in editor
- **WHEN** the user presses `n` on a focused task card
- **THEN** the TUI suspends, the task's notes file is opened in `$EDITOR`, and the TUI resumes after the editor exits

#### Scenario: Create new notes file
- **WHEN** the notes file does not yet exist and the user opens notes for a task
- **THEN** the file is created at `notes/<slug>.md` and opened in the editor

#### Scenario: Edit existing notes file
- **WHEN** the notes file already exists and the user opens notes for a task
- **THEN** the existing file is opened in the editor with its current content

### Requirement: Notes presence indicator on card
Each task card SHALL display a visual indicator (text `[N]` or Unicode `📝`) when a Markdown notes file exists for that task.

#### Scenario: Indicator shown when notes exist
- **WHEN** a task has a corresponding notes file in `notes/`
- **THEN** the task card displays the notes indicator

#### Scenario: No indicator when notes absent
- **WHEN** a task has no corresponding notes file
- **THEN** the task card displays no notes indicator

### Requirement: Slug uniqueness
The slug used to derive the notes filename SHALL be unique within the `notes/` directory. If a collision occurs (two tasks yield the same base slug), a numeric suffix SHALL be appended to the later task's slug.

#### Scenario: Unique slug per task
- **WHEN** two tasks have titles that produce the same base slug
- **THEN** the second task's notes file is named `<slug>-2.md` and the first remains `<slug>.md`
