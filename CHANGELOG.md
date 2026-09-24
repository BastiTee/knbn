# Changelog

## 0.3.1

- Add `--version` flag and keep `db_version` in sync with the package version ([#19](https://github.com/BastiTee/knbn/pull/19))

## 0.3.0

- Add agent-facing CLI with stable task IDs, file locking, and ID-based notes ([#18](https://github.com/BastiTee/knbn/pull/18))
- Write `AGENTS.md` orientation file to the data directory on `knbn init` ([#18](https://github.com/BastiTee/knbn/pull/18))
- Add `--after DATE` filter to `knbn list` ([#18](https://github.com/BastiTee/knbn/pull/18))
- Fix: skip `db_version` write when version is already current ([#18](https://github.com/BastiTee/knbn/pull/18))

## 0.2.0

- Add live task search filter activated with Ctrl+F ([#16](https://github.com/BastiTee/knbn/pull/16))
- Add category color editor with scheme picker to command palette ([#15](https://github.com/BastiTee/knbn/pull/15))
- Improve setup wizard: stop prompting free-text fields once blank, reject duplicate names ([#17](https://github.com/BastiTee/knbn/pull/17))
- Various internal refactors and performance improvements (deduplicated color/regex helpers, cached theme list and notes lookups, fixed double persist on theme confirm)

## 0.1.1

- Fix kanban swimlane toggle to be per-cell, not board-wide ([#14](https://github.com/BastiTee/knbn/pull/14))

## 0.1.0

- Change default categories for new stores to Personal/Work/Other ([#13](https://github.com/BastiTee/knbn/pull/13))
- Preview themes live in a sidebar instead of persisting on every browse ([#11](https://github.com/BastiTee/knbn/pull/11))
- Remove Quit from the command palette ([#12](https://github.com/BastiTee/knbn/pull/12))
- Reduce repaint cost in theme picker, lane toggle, and resize
- Fix demo data categories
- Upgrade all dependencies

## 0.0.4

- Improve release process with proper `uv.lock` commit

## 0.0.3

- Improve build process and release tooling

## 0.0.2

- Add delete and mark-done actions to Tabular and Done views ([#10](https://github.com/BastiTee/knbn/pull/10))
- Fix kanban keyboard focus lost after board mutations ([#9](https://github.com/BastiTee/knbn/pull/9))
- Add `/knbn-release` command for automated releases
- Update README

## 0.0.1

- Initial release
