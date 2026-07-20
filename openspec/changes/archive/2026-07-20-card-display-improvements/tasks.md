## 1. Card CSS

- [x] 1.1 Change `margin: 0 0 1 0` to `margin: 0` in `TaskCard.DEFAULT_CSS` in `src/knbn/widgets/card.py`

## 2. Dynamic title truncation

- [x] 2.1 Remove the hardcoded 30-char truncation from `TaskCard.compose` in `src/knbn/widgets/card.py`
- [x] 2.2 Add a `_title_for_width` helper method that computes available inner width as `max(self.size.width - 4, 8)` (border 1+1 + padding 1+1) and truncates title accordingly
- [x] 2.3 Call `_title_for_width` in `compose` instead of the hardcoded truncation
- [x] 2.4 Add `on_resize` handler to `TaskCard` that calls `self.call_after_refresh(self.recompose)` so the title updates when the terminal is resized

## 3. Spec update

- [x] 3.1 Update `openspec/specs/tui-board/spec.md` — apply the MODIFIED requirement from the change delta (width-aware truncation, single-line spacing)
