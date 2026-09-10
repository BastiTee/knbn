# knbn

**Kanban, but terminal-native and CSV/Markdown-based.**

<img width="1465" height="732" alt="image" src="https://github.com/user-attachments/assets/603b3ec4-4f23-4552-a8d6-d6467761a71a" />

## Features

- **Terminal-native Kanban board** — full task lifecycle (capture, triage, close) without leaving the terminal; no browser required
- **Flat-file CSV and Markdown storage** — tasks live in a single `~/.knbn/` folder; human-readable, version-control friendly, no database
- **Markdown notes per task** — attach a freeform note to any task, opened in your `$EDITOR`
- **Rich TUI powered by Textual** — interactive board with keyboard navigation, modal forms, and live filtering
- **Three views in one tool** — Kanban board (3×3 grid), tabular active-task list, and a "Done this week" archive view
- **Configurable statuses and priorities** — define your own workflow stages and priority levels to match how you actually work
- **Configurable categories** — tag tasks with custom categories and add new ones on the fly
- **Fast CLI capture** — `knbn add --fast --title "..."` adds a task without opening the TUI; pipe-friendly for scripting
- **Zero external services** — no account, no sync server, no cloud dependency; your data stays local and offline
- **Pure Python, uv-managed** — install with a single uv command; typed, linted, and tested; easy to fork or extend

## Install from source

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/BastiTee/knbn.git
cd knbn
make
```

Then run:

```bash
uv run knbn
```

To simplify access, you can put this into your shell-rc:

```
source /path/to/cloned/folder/knbn-rc.sh
```

and after shell restart run:

```
k
```

See [knbn-rc.sh](knbn-rc.sh) for more details.

## License

[Apache License Version 2.0, January 2004](LICENSE.txt)
