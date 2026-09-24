# AGENTS.md

This directory is managed by **knbn**, a terminal-native personal Kanban board.

For full documentation — CLI reference, task fields, configuration format, and
typical agent workflows — see the project README:

> https://github.com/BastiTee/knbn/blob/main/README.md

## Quick orientation

- `knbn --help` — list all available commands
- `knbn config` — read the current board configuration as JSON (valid statuses,
  priorities, categories, and free-text field labels)
- `knbn list --json` — list active tasks as JSON (includes task IDs)
- `tasks.csv` — the task store (use the CLI; do not edit directly)
- `settings.json` — board configuration

You can add project-specific context below this line — it will not be overwritten
by knbn.
