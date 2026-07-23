## Context

Kanban task cards currently display `[N]` when a notes file exists. This is ASCII noise that doesn't stand out clearly. The `key_resource` URL field exists on every task but is only accessible via the detail panel (`o` key). There is no at-a-glance signal on the board that a card has a link.

`TaskCard._notes_indicator()` in `src/knbn/widgets/card.py` is the single place that builds the indicator string. The `key_resource` field is already on the `Task` dataclass and is passed into `TaskCard` via `knbn_task`. The `kanban.py` view already handles `o` in the detail panel via `detail.py`; `webbrowser`/`subprocess.run(['open', ...])` is the pattern already used.

## Goals / Non-Goals

**Goals:**
- Replace `[N]` with `☰` (horizontal lines — visually evokes a document/list)
- Show `※` (reference mark) alongside `☰` when `key_resource` is also set
- Show `※` alone when `key_resource` is set but no notes file exists
- Add `o` keybinding to `KanbanView` to open the focused card's `key_resource` URL

**Non-Goals:**
- Changing indicators in the tabular or closed views (those views don't show `[N]` today)
- Changing any other key bindings or card layout
- Adding link or notes indicators to the detail panel (already shown there as text)

## Decisions

### Decision: Single method handles both indicators
`_notes_indicator()` is renamed/extended to `_card_indicators()` returning the combined suffix string. This keeps all indicator logic in one place and avoids adding a separate `_link_indicator()` that would require the caller to assemble them.

Alternatives: separate methods composed at call site — rejected because it splits a trivially coupled concern.

### Decision: `o` opens URL via `subprocess.run(['open', ...])` mirroring detail.py
`detail.py` already uses `subprocess.run(['open', ...])` (macOS `open`). Using the same approach keeps the codebase consistent without introducing a new import. The no-op branch (no `key_resource`) is a silent return — same behavior as `detail.py`.

Alternatives: `webbrowser.open()` — cross-platform but adds a new import for a tool that targets macOS terminal users. Deferred; easy to change later.

### Decision: Indicator order is `☰ ※` (notes first, link second)
Notes come first because they are the richer, longer-lived artifact. A link is a quick reference; notes are curated. This order is consistent with how the detail panel renders them (notes path before resource URL).

## Risks / Trade-offs

- `☰` and `※` are multi-byte UTF-8 characters; Textual renders them as single display columns on modern terminals. If a terminal doesn't support these glyphs they show as `?` — acceptable degradation.
- The `o` shortcut on the board is currently unbound; no conflict with existing bindings.
- `subprocess.run(['open', ...])` is macOS-specific. Acceptable given the tool's current macOS-only install base; tracked in existing `noqa: S603` suppression already in use.
