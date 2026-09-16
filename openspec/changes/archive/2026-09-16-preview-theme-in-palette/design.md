## Context

`KnbnApp` originally opened the theme picker via Textual's built-in `App.action_change_theme()` → `search_themes()`, which pushes a `CommandPalette(providers=[ThemeProvider])` centered over most of the window. That component was retained for the first cut of preview/persist/revert semantics, but it visually covers most of the screen, which is a poor fit for a quick "browse and preview" interaction — see proposal.md for the follow-up request that replaced it.

The picker is now a purpose-built `ThemeSidebar` (`src/knbn/widgets/theme_sidebar.py`), a `ModalScreen` whose only child is a plain Textual `OptionList` docked to the right edge (`dock: right`, `width: 33%` clamped to `min-width: 30` / `max-width: 60`), styled the same way Textual's own built-in keys help panel (`KeyPanel`, `split: right`) docks to the side rather than covering the window. The `ModalScreen`'s own background is `transparent`, so only the docked list is visible — the rest of the board stays on screen behind it, dimmed by nothing.

`KnbnApp.watch_theme` persists to `settings.json` on every assignment to `self.theme` with no distinction between "user is browsing" and "user confirmed" unless told otherwise — see the preview-flag mechanism below.

## Goals / Non-Goals

**Goals:**
- Live preview: moving the highlight in the sidebar applies each highlighted theme to the running app immediately.
- No spurious writes: only a confirmed selection is written to `settings.json`.
- Clean cancel: escaping the sidebar restores exactly the theme that was active before it opened.
- The picker occupies a bounded strip of the window (a sidebar), not most of the screen.

**Non-Goals:**
- Re-implementing fuzzy search over theme names — the sidebar lists all themes; there are few enough that search isn't needed.
- Changing the `settings.json` schema or `app-settings`/`board-config` code.

## Decisions

**Replace the built-in `CommandPalette`/`ThemeProvider` picker with a custom `ThemeSidebar(ModalScreen[None])` built directly on `OptionList`.** Textual's `CommandPalette` is a centered, near-full-width overlay by design (`CommandPalette { align: center middle; ... }`), and there's no supported way to make it dock to an edge instead — its layout is baked into the widget's own CSS and structure. Building a small dedicated screen around `OptionList` (which already provides cursor navigation, highlighting, and selection out of the box) gives full control over layout while reusing Textual's built-in list-navigation bindings (`up`/`down`/`home`/`end`/`enter`).

**Give `KnbnApp` a small public API (`preview_theme`, `confirm_theme`) instead of routing through `CommandPalette`-specific messages.** `ThemeSidebar` calls `self.app.preview_theme(name)` on `OptionList.OptionHighlighted` and `self.app.confirm_theme(name)` on `OptionList.OptionSelected`; `action_cancel` (bound to `Escape`) calls `self.app.preview_theme(original_theme)` to revert. This removes the earlier `CommandPalette.OptionHighlighted`/`CommandPalette.Closed` app-level message handlers and the `_theme_before_preview` bookkeeping entirely — the sidebar screen owns its own "original theme" (passed into its constructor), so there's no cross-message-type guarding needed against the unrelated `Ctrl+P` system command palette (`ThemeSidebar` and the system `CommandPalette` are now unrelated screen types).

**Keep the preview-flag mechanism on `KnbnApp` (`_theme_preview_active`, `_persist_theme`).** `preview_theme` sets the flag, assigns `self.theme`, then clears it; `watch_theme` skips persistence while the flag is set. `confirm_theme` assigns `self.theme` and persists explicitly via `_persist_theme`, rather than relying on `watch_theme` to fire — the confirmed value is always the value already live-previewed, so Textual's reactive sees no change and would otherwise skip the watcher entirely (this was verified while testing the original `CommandPalette`-based implementation and still applies here).

## Risks / Trade-offs

- [Risk] A plain `OptionList` has no fuzzy search, so finding a specific theme among many requires scrolling/arrowing instead of typing to filter. → Mitigation: accepted for now given the built-in theme count is small; explicitly a non-goal above.
- [Risk] If the app is closed while a preview is active and not yet reverted, the in-memory `self.theme` differs from `settings.json`, but since the process is exiting and nothing further reads `self.theme`, `settings.json` was never written, so this is not a risk to persisted state.
- [Risk] `KnbnApp.CSS` sets a bare `Screen { background: $surface; }` rule. Textual applies App-level CSS with higher priority than a widget's own `DEFAULT_CSS` regardless of selector specificity, so `ThemeSidebar`'s own `background: transparent` (set in its `DEFAULT_CSS`) was silently overridden by that rule — the sidebar rendered as a fully opaque full-screen panel, hiding the board behind it entirely, even though the docked `OptionList` itself only occupied the right third. Caught via a screenshot-based test (`export_screenshot()` before/after opening the sidebar, checking for board text) and confirmed as a CSS-cascade issue, not a layout one. → Mitigation: add a matching `ThemeSidebar { background: transparent; }` rule directly into `KnbnApp.CSS` itself, after the generic `Screen` rule — same stylesheet, same specificity, later declaration wins the cascade tie. Any future `ModalScreen` subclass that needs a non-default background must do the same (override in `KnbnApp.CSS`, not just the widget's own `DEFAULT_CSS`).

## Migration Plan

No data migration. Existing `settings.json` files are unaffected. Behavior change is purely in-session (TUI process), so no rollback beyond reverting the code.
