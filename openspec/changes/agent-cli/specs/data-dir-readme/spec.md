## Purpose

A boilerplate `README.md` written to the knbn data directory on initialization that gives agents (and humans) a discoverable reference for the CLI, data layout, and task fields — analogous to `CLAUDE.md` for Claude Code projects. Users can freely edit it to add project-specific context.

## ADDED Requirements

### Requirement: README.md written on data directory init
When `ensure_data_dir` initializes a new data directory it SHALL write a `README.md` file from a bundled template. If a `README.md` already exists in the data directory it SHALL NOT be overwritten, preserving any user edits.

#### Scenario: README.md created on fresh init
- **WHEN** `ensure_data_dir` is called on a directory that does not yet contain `README.md`
- **THEN** `README.md` is written to the data directory

#### Scenario: Existing README.md is not overwritten
- **WHEN** `ensure_data_dir` is called and `README.md` already exists in the data directory
- **THEN** the file is left unchanged

### Requirement: README.md template content
The bundled template SHALL cover at minimum:

- A one-paragraph summary of what knbn is and where this directory lives.
- The full list of task fields (ID, title, status, priority, category, due, key_resource, free_text_1–3, date_created, date_modified) with a one-line description of each.
- The core CLI commands an agent needs: `knbn add`, `knbn list`, `knbn edit`, `knbn delete`, `knbn config`.
- A note that `settings.json` holds board configuration (statuses, priorities, categories) and that `knbn config` emits it as JSON.
- A note that users can edit this file to add project-specific context visible to agents.

#### Scenario: Template covers task fields
- **WHEN** `README.md` is read from a freshly initialized data directory
- **THEN** the file mentions all twelve task field names

#### Scenario: Template covers CLI commands
- **WHEN** `README.md` is read from a freshly initialized data directory
- **THEN** the file mentions `knbn add`, `knbn list`, `knbn edit`, `knbn delete`, and `knbn config`

### Requirement: Template is bundled with the package
The README template SHALL be stored as a resource file inside the `knbn` package (e.g. `src/knbn/defaults/README.md`) so it is available after installation without requiring network access or the source tree.

#### Scenario: Template is readable after install
- **WHEN** the knbn package is installed and `ensure_data_dir` is called
- **THEN** `README.md` is written without error regardless of whether the source tree is present
