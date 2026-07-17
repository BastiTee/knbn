## 1. Create demo directory structure

- [x] 1.1 Create `demo/notes/.gitkeep`
- [x] 1.2 Write `demo/tasks.csv` with header + 12–15 active tasks (Now/Feedback/Todo × High/Medium/Low) and 25–30 terminal tasks (Done/Delegated/Stopped) covering all categories and featuring fictional names

## 2. Verify

- [x] 2.1 Run `KNBN_DATA_DIR=demo uv run knbn board` and confirm the board loads without errors (spot-check via CLI `uv run knbn board` in test mode isn't feasible headlessly, so verify CSV loads cleanly via `uv run python -c "from knbn.model.store import load_tasks; from pathlib import Path; t=load_tasks(Path('demo')); print(len(t), 'tasks')"`)
- [x] 2.2 Run `make build` to confirm no regressions
