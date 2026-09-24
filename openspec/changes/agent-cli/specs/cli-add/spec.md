## ADDED Requirements

### Requirement: JSON output for add
The `knbn add` command SHALL support a `--json` flag. When set, the command SHALL print the created task as a JSON object to stdout instead of the human-readable `✓ Task added: <title>` confirmation. The JSON object SHALL include all task fields including the assigned `id`.

#### Scenario: JSON output after add
- **WHEN** `knbn add --fast --title "My task" --json` is called
- **THEN** stdout is a valid JSON object representing the created task with a non-empty `id` field

#### Scenario: Human output unchanged without --json
- **WHEN** `knbn add --fast --title "My task"` is called without `--json`
- **THEN** stdout is `✓ Task added: My task` (unchanged behavior)
