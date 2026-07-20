## Context

`TaskCard.compose` in `src/knbn/widgets/card.py` renders the title line with a hardcoded 30-character truncation (line 73). The three Kanban columns each take `1fr` of the terminal width, so at a typical 120-column terminal each column is ~40 characters wide — meaning 10+ characters of the card interior are always wasted. The CSS also applies `margin: 0 0 1 0` which adds a blank line after each card border, producing a two-line visual gap between consecutive cards.

## Goals / Non-Goals

**Goals:**
- Truncate card titles dynamically to the card's actual rendered inner width.
- Reduce inter-card spacing to a single border row (no extra margin).

**Non-Goals:**
- Reflowing multi-line titles.
- Changing any other card fields (category tag, due date).
- Altering column widths or the overall 3-column layout.

## Decisions

### Dynamic title width via `on_resize` / `size`

Textual exposes the rendered widget size as `self.size.width` after mount. The inner width available for text is `self.size.width - 4` (2 chars for round border on each side + 1 char padding on each side as set by `padding: 0 1`).

**Chosen approach**: override `on_resize` (and `on_mount`) to recompute the title truncation whenever the widget size changes, then call `self.refresh()`. Store the computed title on the widget and use it in `render` instead of `compose`, or keep `compose` and call `self.recompose()`.

**Simpler alternative**: override `render()` on the title `Static` child. Ruled out — `TaskCard` uses two `Static` children, complicating subclassing.

**Chosen implementation**: Replace the two `Static` children in `compose` with a single `render()` method that computes available width from `self.size.width` at render time. This avoids needing `on_resize` callbacks or recompose cycles — Textual calls `render()` whenever the widget redraws, which includes after resize.

However, `TaskCard` inherits from `Static` (which has a single `render`). Since we yield two lines (title + tag/due), we keep the `compose` approach but compute the truncation from `self.size.width` at compose time. We add `on_resize` to trigger `recompose()` so the title updates on terminal resize.

### Bottom margin removal

Change `margin: 0 0 1 0` to `margin: 0` in `TaskCard.DEFAULT_CSS`. The round border already provides one line of visual separation — no extra margin needed.

## Risks / Trade-offs

- **Recompose on every resize**: calling `self.call_after_refresh(self.recompose)` in `on_resize` means each terminal resize event triggers a full card recompose. This is acceptable for a personal tool with at most ~30 cards on screen; it would not be acceptable for a high-frequency data grid.
- **Border+padding math**: the formula `self.size.width - 4` assumes `border: round` (1 char each side) and `padding: 0 1` (1 char each side). If either changes in CSS, the formula must be updated. A comment will document this dependency.

## Migration Plan

No data migration needed. Pure visual change; existing CSV files unaffected.

## Open Questions

None.
