## MODIFIED Requirements

### Requirement: Notes file creation and editing
The system SHALL allow creating and editing a per-task Markdown notes file via the TUI (key `n` on a focused card or in the detail panel) or via `knbn add`. The file SHALL be opened in the editor specified by `$EDITOR`, falling back to `nano` if unset. After the editor exits, if the file was newly created during this session and its content contains no non-whitespace characters, the file SHALL be deleted automatically.

#### Scenario: Open notes in editor
- **WHEN** the user presses `n` on a focused task card
- **THEN** the TUI suspends, the task's notes file is opened in `$EDITOR`, and the TUI resumes after the editor exits

#### Scenario: Create new notes file
- **WHEN** the notes file does not yet exist and the user opens notes for a task
- **THEN** the file is created at `notes/<slug>.md` and opened in the editor

#### Scenario: Edit existing notes file
- **WHEN** the notes file already exists and the user opens notes for a task
- **THEN** the existing file is opened in the editor with its current content

#### Scenario: Discard newly created blank notes file
- **WHEN** the notes file did not exist before the editor was opened AND the user saves and exits the editor without entering any non-whitespace content
- **THEN** the file is deleted so no empty notes file persists and no notes indicator appears on the card

#### Scenario: Preserve existing file cleared to blank
- **WHEN** the notes file existed before the editor was opened AND the user clears all content and exits
- **THEN** the file is left as-is (not deleted)
