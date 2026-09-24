# AGENTS.md

This directory is managed by **knbn**, a terminal-native personal Kanban board.

For full documentation — CLI reference, task fields, configuration format, and
typical agent workflows — see the project README. The correct URL is version-specific:

1. Run `knbn config` and read the `db_version` field from the output.
2. Navigate to `https://github.com/BastiTee/knbn/blob/<db_version>/README.md`

Example: if `db_version` is `0.2.1`, the README is at
`https://github.com/BastiTee/knbn/blob/0.2.1/README.md`.

## Quick orientation

- `knbn --help` — list all available commands
- `knbn config` — read the current board configuration as JSON (valid statuses,
  priorities, categories, free-text field labels, and `db_version`)
- `knbn list --json` — list active tasks as JSON (includes task IDs)
- `knbn list --after YYYY-MM-DD --json` — limit output to tasks modified on or after a date (keeps context small)
- `tasks.csv` — the task store (use the CLI; do not edit directly)
- `settings.json` — board configuration

You can add project-specific context below this line — it will not be overwritten
by knbn.
