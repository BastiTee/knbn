## Context

The footer toolbar is rendered by Textual's `Footer` widget, which displays bindings from the active screen. The three view-switching bindings (`1 Kanban`, `2 Tabular`, `3 Closed`) are declared in `KnbnApp.BINDINGS`. Currently they are all styled identically regardless of which view is active, leaving the user with no visual orientation cue.

`KnbnApp._show_view` already tracks the active view as a string passed to the method, but the app has no reactive that exposes it to the UI.

## Goals / Non-Goals

**Goals:**
- The active tab key in the footer is visually distinct (e.g. bold or accent-coloured) from inactive tab keys
- The highlight updates immediately whenever the active view changes
- The approach uses idiomatic Textual patterns (reactive variable + CSS class) to avoid fragile workarounds

**Non-Goals:**
- Changing the footer layout or adding new UI elements
- Highlighting non-tab bindings (q, a, ?)
- Persisting the last-active tab across restarts (already done implicitly via kanban-first mount)

## Decisions

### Use a reactive string + CSS pseudo-class on the Footer via custom binding labels

**Decision:** Introduce `_active_view: reactive[str]` on `KnbnApp`. Override the Footer's rendering by replacing the standard `BINDINGS` approach with a custom `Footer`-subclass or by toggling a CSS class on the app that selects specific footer keys.

**Preferred approach — custom Footer subclass with `_active_view`-aware rendering:** Textual's built-in `Footer` renders each binding as a `FooterKey` widget (internal). The most stable and forward-compatible approach is to add a CSS class to the `App` (e.g. `view-kanban`, `view-tabular`, `view-closed`) and write CSS rules that target the footer key labels by their binding key character.

Textual's `Footer` renders binding keys as `Footer > .footer--highlight` / `Footer > .footer--key` spans. The key label text (the character, e.g. `1`) is not directly addressable by a stable CSS selector without subclassing.

**Simplest working approach:** Subclass `Footer` to override `_make_key_text` (or equivalent), inject the active view from the app, and render the active tab key with an `$accent` colour or bold style. This keeps implementation self-contained in `app.py`.

**Alternative considered — Rich markup in binding descriptions:** Binding descriptions can contain Rich markup. Dynamically updating `BINDINGS` at runtime is not supported cleanly. Rejected.

**Alternative considered — Reactive CSS class on App root:** Adding `app.add_class("view-kanban")` and CSS like `.view-kanban Footer ._footer-key-1 { color: $accent; }` would work if Textual assigns stable per-key classes. Textual does assign a `--binding-key` data attribute but not a stable CSS class per key. Rejected as fragile.

**Chosen approach:** Subclass `Footer` as `KnbnFooter`. Track active view via `reactive` on `KnbnApp`. Pass the active view name into `KnbnFooter` via a reactive attribute. Override `render_key` (or use `watch_`) to apply bold/accent styling to the matching key.

In practice the simplest Textual-idiomatic path is:
1. Add `_active_view: reactive[str] = reactive("kanban")` to `KnbnApp`
2. Update it in `_show_view`
3. Write CSS targeting `Footer .footer--key` where the key value matches the active tab — achieved by giving the Footer a reactive-driven class like `active-1`, `active-2`, `active-3` and writing three CSS rules

## Risks / Trade-offs

- **Textual internal CSS class names may change between versions.** Mitigation: use the public `add_class`/`remove_class` API on the `Footer` widget rather than targeting internal pseudo-class names directly; test after Textual upgrades.
- **Minimal visual change.** The highlight must be subtle enough not to clash with themes. Using `text-style: bold` only (no colour) is the safest cross-theme choice; alternatively `color: $accent` is theme-aware.
