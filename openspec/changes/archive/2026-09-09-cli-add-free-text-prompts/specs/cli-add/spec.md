## MODIFIED Requirements

### Requirement: knbn add command
The system SHALL provide a `knbn add` subcommand that captures a new task interactively from the terminal. The prompt sequence SHALL be: title (required, free text) → status (numbered selection, default is the first configured active status) → priority (numbered selection, default `Medium`) → category (numbered selection from known categories, default is the last configured category) → key resource (URL, optional, Enter to skip) → one optional prompt per active free-text field (in `BoardConfig.free_text_fields` index order, skippable with Enter). Only fields whose label is non-empty in `BoardConfig.free_text_fields` SHALL be prompted. After saving, the command SHALL print `✓ Task added: <title>` and exit.

#### Scenario: Full interactive add
- **WHEN** `knbn add` is run with no flags and the user answers all prompts
- **THEN** a task is appended to `tasks.csv` with the provided values and a confirmation message is printed

#### Scenario: Skip key resource
- **WHEN** the user presses Enter at the Key Resource prompt
- **THEN** `key_resource` is stored as empty string

#### Scenario: Free-text field prompt uses configured label
- **WHEN** `free_text_fields` is `['Feedback From', '', 'Notes']` and the user runs `knbn add`
- **THEN** prompts appear for `Feedback From` (index 0) and `Notes` (index 2); no prompt appears for index 1

#### Scenario: Skip free-text field with Enter
- **WHEN** the user presses Enter at a free-text field prompt
- **THEN** the corresponding `free_text_N` field is stored as empty string

#### Scenario: No free-text prompts when no active fields configured
- **WHEN** `free_text_fields` is `['', '', '']` (all empty labels)
- **THEN** no free-text prompts appear and the task is saved with all free-text fields empty

## MODIFIED Requirements

### Requirement: Quick-add flags
The `knbn add` command SHALL support the following flags: `--title TEXT` (pre-fills title, skips title prompt), `--status-default` (use the first configured active status, skip status prompt), `--priority-default` (use `Medium`, skip priority prompt), `--category-default` (use the last configured category, skip category prompt), `--no-resource` (skip key resource prompt), `--no-free-text` (skip all free-text field prompts), `--fast` / `-f` (equivalent to all four `--*-default` flags plus `--no-resource` and `--no-free-text`).

#### Scenario: Fast flag skips all prompts except title
- **WHEN** `knbn add --fast` is run
- **THEN** only the title prompt is shown; all other fields use defaults

#### Scenario: Pre-filled title with fast flag
- **WHEN** `knbn add --fast --title "My task"` is run
- **THEN** no prompts are shown and the task is saved immediately with defaults

#### Scenario: no-free-text flag skips free-text prompts
- **WHEN** `knbn add --no-free-text` is run with active free-text fields configured
- **THEN** no free-text prompts appear and all free-text fields are stored as empty string
