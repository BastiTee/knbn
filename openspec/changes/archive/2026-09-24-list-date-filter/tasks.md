## 1. CLI — add --after flag

- [x] 1.1 Add `--after` option to `list_tasks` in `src/knbn/cli.py`; parse with `parse_datetime`, raise `click.BadParameter` if the value cannot be parsed; filter tasks where `parse_datetime(task.date_modified)` returns a datetime >= the parsed threshold; verify with `knbn list --after 2099-01-01` returning no tasks and `knbn list --after 2000-01-01` returning all active tasks

## 2. Tests

- [x] 2.1 Add tests in `tests/test_cli.py` covering: `--after` with a date that matches some tasks, `--after` combined with `--status`, `--after` with `--json`, `--after` with a future date returning empty result, and `--after "not-a-date"` exiting non-zero

## 3. Final verification

- [x] 3.1 Run `make build` and confirm it passes with no new type errors, lint violations, or coverage regressions
