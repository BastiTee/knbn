## ADDED Requirements

### Requirement: First-run wizard trigger
The system SHALL run an interactive CLI setup wizard when `knbn init` or `knbn board` is called and both of the following conditions are true: (a) `tasks.csv` does not exist in the data directory, and (b) `settings.json` in the data directory does not contain a `board` key. If either condition is false, the wizard SHALL be skipped silently.

#### Scenario: Wizard runs on blank slate
- **WHEN** the data directory is empty (no `tasks.csv`, no `settings.json`) and `knbn init` is called
- **THEN** the setup wizard starts interactively

#### Scenario: Wizard skipped when tasks exist
- **WHEN** `tasks.csv` exists in the data directory (even if `settings.json` has no `board` key)
- **THEN** the wizard is skipped and the board launches with synthesized defaults

#### Scenario: Wizard skipped when board config exists
- **WHEN** `settings.json` contains a `board` key
- **THEN** the wizard is skipped regardless of whether `tasks.csv` exists

### Requirement: Active status configuration step
The wizard SHALL prompt the user to enter 2–5 active status names, one per line, with a blank line to finish. The first entry SHALL automatically become the default active status (leftmost column on the board). The wizard SHALL reject input with fewer than 2 or more than 5 entries, and SHALL reject any individual name shorter than 2 or longer than 15 characters, displaying a clear error and re-prompting in each case.

#### Scenario: Two active statuses accepted
- **WHEN** the user enters two status names and a blank line
- **THEN** the wizard records both statuses and sets the first as default active status

#### Scenario: One active status rejected
- **WHEN** the user enters one status name and a blank line
- **THEN** the wizard displays an error message and re-prompts

#### Scenario: Six active statuses rejected
- **WHEN** the user enters six status names
- **THEN** the wizard displays an error message and re-prompts

#### Scenario: Status name too short rejected
- **WHEN** the user enters a single-character status name
- **THEN** the wizard displays an error message and re-prompts

#### Scenario: Status name too long rejected
- **WHEN** the user enters a status name longer than 15 characters
- **THEN** the wizard displays an error message and re-prompts

### Requirement: Terminal status configuration step
The wizard SHALL prompt the user to enter 1–3 terminal (done/archived) status names. The wizard SHALL ask which one is the default terminal status (used for the quick "mark done" action). The wizard SHALL reject fewer than 1 or more than 3 entries, and SHALL reject any individual name shorter than 2 or longer than 15 characters.

#### Scenario: Single terminal status accepted
- **WHEN** the user enters one terminal status name
- **THEN** it is recorded as both the only terminal status and the default terminal status

#### Scenario: Default terminal status selection
- **WHEN** the user enters multiple terminal statuses and selects one as default
- **THEN** `default_terminal_status` in config matches the selection

### Requirement: Priority configuration step
The wizard SHALL prompt the user to enter 1–5 priority names in order from highest to lowest. The wizard SHALL reject fewer than 1 or more than 5 entries, and SHALL reject any individual name shorter than 2 or longer than 15 characters.

#### Scenario: Valid priority list accepted
- **WHEN** the user enters three priority names in order
- **THEN** all three are recorded as `priorities` in the board config

### Requirement: Category configuration step
The wizard SHALL prompt the user to enter 1–10 category names. Colors SHALL be auto-assigned from the fixed palette defined in the board-config spec and SHALL NOT be asked for during the wizard. The wizard SHALL reject fewer than 1 or more than 10 entries, and SHALL reject any individual name shorter than 2 or longer than 15 characters.

#### Scenario: Categories auto-colored
- **WHEN** the user enters three category names during the wizard
- **THEN** each category is stored with an auto-assigned hex color from the palette

### Requirement: Free-text field configuration step
The wizard SHALL prompt the user to enter 0–3 free-text field labels (additional per-task text fields shown in the edit form). Entering a blank line for a slot means that slot is unused. The wizard SHALL reject more than 3 entries.

#### Scenario: Zero free-text fields accepted
- **WHEN** the user presses Enter immediately (blank) for the first free-text field prompt
- **THEN** `free_text_fields` is stored as `['', '', '']` and no free-text inputs appear in the task form

### Requirement: Wizard completion
On successful completion, the wizard SHALL write the collected board config to `settings.json` (creating the file if absent), print a confirmation message, and return. The `knbn init` command SHALL then complete normally; the `knbn board` command SHALL proceed to launch the TUI.

#### Scenario: Config persisted after wizard
- **WHEN** the wizard completes with valid input
- **THEN** `settings.json` contains a `board` key with all configured values

#### Scenario: Board launches after wizard in `knbn board` flow
- **WHEN** the wizard completes during `knbn board`
- **THEN** the TUI launches immediately with the new config applied
