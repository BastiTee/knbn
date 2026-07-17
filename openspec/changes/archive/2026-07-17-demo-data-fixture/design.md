## Context

`knbn` reads from `~/.knbn/tasks.csv` by default, or from `$KNBN_DATA_DIR/tasks.csv` when the env var is set. The CSV column order is fixed: `Name,Category,Date Created,Delegated To,Due,Feedback From,Key Resource,Last edited time,Priority,Status`. Dates use the format `Month D, YYYY H:MM AM/PM` (e.g. `July 3, 2026 9:15 AM`). All seven categories are used (`People`, `Hiring`, `Strategy`, `Product`, `Engineering`, `Work Life`, `Ideas`).

The demo should feel like a real EM's board: a mix of 1:1 prep, hiring pipeline, incident follow-ups, roadmap items, and personal organisation — not generic placeholder text.

## Goals / Non-Goals

**Goals:**
- Commit a `demo/tasks.csv` with ~40–45 rows (header + tasks) covering every status, priority, and category combination.
- Include fictional but plausible names: engineers `Alex Chen`, `Priya Nair`, `Marcus Webb`; teams `Platform`, `Growth`, `Data Infra`; candidates `Jordan Lee`, `Sam Okafor`.
- `demo/notes/` directory with a `.gitkeep` so git tracks it.
- Usage documented in a brief comment at the top of the CSV is not feasible (no comments in CSV), so the task list covers adding a note to `README.md` or similar.

**Non-Goals:**
- Generating actual Markdown note files in `demo/notes/`.
- Any code changes.

## Decisions

**Hand-craft the CSV rather than generating it programmatically**

The dataset is small (≤50 rows) and needs to feel authentic. Hard-coding it is faster, more readable in review, and avoids adding a generation script that has no other use.

**Date spread: past 6 weeks**

Active tasks get `Date Created` in the last 2–3 weeks; terminal tasks span 6 weeks back to give a realistic Done-by-week view with multiple week groups.

**No real URLs in Key Resource**

Use plausible-looking but non-functional URLs like `https://linear.app/acme/issue/ENG-412` to avoid accidentally linking to real pages.
