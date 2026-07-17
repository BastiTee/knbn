## Why

Showing the tool to someone without exposing personal tasks requires a ready-made demo dataset. Currently there is no way to launch `knbn` with realistic-looking data without pointing it at real work. A `demo/` directory with a pre-populated `tasks.csv` lets anyone run `KNBN_DATA_DIR=demo uv run knbn board` and see a fully populated board immediately.

## What Changes

- New `demo/` directory at the repo root containing a `tasks.csv` with:
  - 10–15 active tasks spanning all three statuses (`Now`, `Feedback`, `Todo`) and all three priorities (`High`, `Medium`, `Low`), across all categories
  - 20–30 terminal tasks (`Done`, `Delegated`, `Stopped`) representing realistic closed work from the past few weeks
  - Fictional engineer/engineering manager names and team names throughout
- A `demo/notes/` subdirectory (empty, satisfies the data-dir contract)
- `demo/` is added to `.gitignore`… actually no — it should be committed so it's always available. No `.gitignore` entry needed.

## Capabilities

### New Capabilities

*(none — this is a data file, no code changes)*

### Modified Capabilities

*(none)*

## Impact

- New file: `demo/tasks.csv`
- New directory: `demo/notes/` (empty, created by `ensure_data_dir` on first run, so just a placeholder note in README or a `.gitkeep`)
- Usage: `KNBN_DATA_DIR=demo uv run knbn board`
