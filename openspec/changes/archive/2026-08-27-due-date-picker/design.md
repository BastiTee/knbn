## Context

The Due field in `TaskForm` is a plain `Input` widget. Users must type dates in `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` format from memory or by consulting an external calendar. There is also no visual indication on the Due field itself when its value is invalid — only a text message appears below it.

## Goals / Non-Goals

**Goals:**
- Add a `DateTimePicker` modal that opens from the Due field via `Enter`.
- Navigate the calendar and confirm a date using only keys already present in the app (arrows, Enter, Esc, Tab).
- Pre-fill the picker from a valid existing value; show an error and block opening when the value is invalid.
- Add a CSS error-highlight class to the Due field itself (border colour) on validation failure.
- Support mouse clicks on calendar day cells as a convenience.

**Non-Goals:**
- A generic reusable picker for other fields (only the Due field uses it initially).
- Time zones, locale formatting, or custom date ranges.
- Animated transitions.

## Decisions

**1. Single-modal, calendar + time together**

The picker shows a calendar grid and a `HH:MM` text input in one `ModalScreen`. Alternative (two-step: calendar then time) was rejected — it adds a step and makes it harder to review both at once.

**2. Month navigation via arrow wrap-around — no new keys**

Left/right arrows move day-by-day; crossing a month boundary auto-advances the month. Up/down move week-by-week. This means month navigation is implicit — no new `PgUp`/`[`/`]` keys needed. The calendar header shows `< YYYY-MM >` as read-only context.

**3. `DueInput(Input)` subclass intercepts `Enter`**

`TaskForm` replaces the plain Due `Input` with a `DueInput` subclass. `DueInput` overrides `_on_key`: when `Enter` is pressed, it posts a `DueInput.EnterPressed` message instead of the default submit behaviour. The form handles this message to validate the field value and conditionally open the picker.

Alternative (binding at form level) was rejected — Textual gives `Input` higher priority for `Enter`, making it unreliable to intercept at the parent level without subclassing.

**4. Error highlight via CSS class on the input**

On validation failure (either from a save attempt or from an `Enter` press on an invalid value), the form adds the CSS class `--invalid` to `DueInput`. The class applies `border: tall $error`. This is removed when the user starts editing the field again (`on_input_changed`).

**5. Picker returns `str | None`**

`DateTimePicker` is a `ModalScreen[str | None]`. It returns the formatted date string on confirm, `None` on cancel. The form writes the return value back into `DueInput`.

**6. Time row is always visible but optional**

An `HH:MM` input row is shown below the calendar. It is pre-filled if a time component is present in the existing value, otherwise empty. Leaving it empty produces a date-only result. Up/down arrows on hour/minute digits increment/decrement the value when the time input is focused.

## Risks / Trade-offs

- [Textual `Input` key interception is fragile across versions] → Use a dedicated subclass with `_on_key` rather than bindings, and pin to the tested Textual version.
- [Arrow wrap-around at month boundary is unintuitive to some users] → The calendar header always shows the current month/year so context is clear; this is how most mobile date pickers work.
- [Time input is a free-text `HH:MM` field, not spinners] → Simpler to implement and consistent with the existing Due text field. Validation is applied on confirm.
