# cli-add

## Purpose

CLI subcommands for adding tasks and launching the board from the terminal.

## Requirements

### Requirement: knbn add command
The system SHALL provide a `knbn add` subcommand that captures a new task interactively from the terminal. The prompt sequence SHALL be: title (required, free text) → status (numbered selection, default `Todo`) → priority (numbered selection, default `Medium`) → category (numbered selection from known categories, default `Ideas`) → key resource (URL, optional, Enter to skip). After saving, the command SHALL print `✓ Task added: <title>` and exit.

#### Scenario: Full interactive add
- **WHEN** `knbn add` is run with no flags and the user answers all prompts
- **THEN** a task is appended to `tasks.csv` with the provided values and a confirmation message is printed

#### Scenario: Skip key resource
- **WHEN** the user presses Enter at the Key Resource prompt
- **THEN** `key_resource` is stored as empty string

### Requirement: Conditional prompts for Feedback and Delegated statuses
The system SHALL ask for `Feedback From` when the user selects `Feedback` status, and for `Delegated To` when the user selects `Delegated` status. These additional prompts SHALL NOT appear for other statuses.

#### Scenario: Feedback From prompt
- **WHEN** the user selects `Feedback` as status
- **THEN** the system additionally prompts for `Feedback From` (free text)

#### Scenario: No extra prompt for Todo
- **WHEN** the user selects `Todo` as status
- **THEN** no extra prompts appear beyond the standard sequence

### Requirement: Quick-add flags
The `knbn add` command SHALL support the following flags: `--title TEXT` (pre-fills title, skips title prompt), `--status-default` (use `Todo`, skip status prompt), `--priority-default` (use `Medium`, skip priority prompt), `--category-default` (use `Ideas`, skip category prompt), `--no-resource` (skip key resource prompt), `--fast` / `-f` (equivalent to all four `--*-default` flags plus `--no-resource`).

#### Scenario: Fast flag skips all prompts except title
- **WHEN** `knbn add --fast` is run
- **THEN** only the title prompt is shown; all other fields use defaults

#### Scenario: Pre-filled title with fast flag
- **WHEN** `knbn add --fast --title "My task"` is run
- **THEN** no prompts are shown and the task is saved immediately with defaults

### Requirement: knbn board command
The system SHALL provide a `knbn board` subcommand (also callable as `knbn` with no subcommand) that launches the full TUI board.

#### Scenario: Launch board
- **WHEN** `knbn board` is executed
- **THEN** the TUI application starts and displays the Kanban view

### Requirement: knbn init command
The system SHALL provide a `knbn init [PATH]` subcommand that initializes the data directory. If the directory already exists, the command SHALL print the existing path and exit without error.

#### Scenario: Init creates data directory
- **WHEN** `knbn init` is called and `~/.knbn/` does not exist
- **THEN** the directory, `tasks.csv`, and `notes/` are created

#### Scenario: Init is idempotent
- **WHEN** `knbn init` is called and the data directory already exists
- **THEN** no error is raised and the existing path is printed
