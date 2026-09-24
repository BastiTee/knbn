## Why

Agents querying `knbn list` receive every active task in the store, which grows unbounded over time. A date-based filter lets an agent ask only for tasks that have had recent activity, keeping context payloads small and predictable.

## What Changes

- **CHANGED** `knbn list` gains a `--after DATE` flag that limits output to tasks whose `date_modified` is on or after the given date. The flag is orthogonal to all existing filters (`--status`, `--priority`, `--category`, `--all`, `--json`).

## Capabilities

### New Capabilities

_(none)_

### Modified Capabilities

- `cli-list`: adds `--after DATE` filter requirement to the existing `knbn list` command.

## Impact

- `src/knbn/cli.py` — add `--after` option to the `list_tasks` command; filter using the existing `parse_datetime` helper.
- `tests/test_cli.py` — new tests for `--after` with valid dates, combined filters, and invalid date input.
