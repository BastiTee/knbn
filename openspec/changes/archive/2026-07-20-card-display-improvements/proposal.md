## Why

Task cards on the Kanban board truncate titles at a hardcoded 30-character limit regardless of the actual column width available, wasting most of the horizontal space in wider terminals. Cards also carry an extra blank line between them (1-cell bottom margin on top of two border rows), making the board feel vertically bloated.

## What Changes

- Task card titles SHALL be truncated to fit the actual available column width rather than a fixed 30-character ceiling, keeping equal left and right margins within the card border.
- The visual gap between consecutive cards in a column SHALL be reduced to a single border row (no extra margin line).

## Capabilities

### New Capabilities

_(none — this is a visual polish change to an existing capability)_

### Modified Capabilities

- `tui-board`: Card rendering requirements change — title truncation must be width-aware, and inter-card spacing is reduced.

## Impact

- `src/knbn/widgets/card.py`: `TaskCard.compose` and CSS — remove hardcoded truncation, add resize-aware rendering, reduce bottom margin.
- `openspec/specs/tui-board/spec.md`: Update the Kanban card rendering requirement to reflect width-aware truncation and single-line spacing.
