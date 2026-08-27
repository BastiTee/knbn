## Why

Manually typing a due date requires the user to context-switch to an external calendar to confirm the correct date, slowing down task creation. An inline date/time picker surfaces a navigable calendar and time selector directly in the form.

## What Changes

- Pressing `Enter` on the Due field opens an inline date/time picker overlay.
  - If the field is empty, the picker opens at today's date with no time.
  - If the field contains a valid date/datetime, the picker opens pre-filled with that value.
  - If the field contains an invalid value, the existing validation error is shown and the picker does NOT open.
- The picker is a two-step overlay: first a calendar month view (select date), then an optional time input row (hour:minute).
- Confirming the picker writes the selected value back into the Due field in `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` format.
- The picker is fully keyboard-driven (arrows navigate, `Enter` confirms/advances, `Esc` cancels) and also supports mouse clicks.
- Error styling on the Due field is added: the field border turns red when a validation error is active (currently there is no field-level error highlight, only the text message below).

## Capabilities

### New Capabilities

- `date-time-picker`: An inline overlay widget for picking a calendar date and optionally a time, usable from any form input field.

### Modified Capabilities

- `tui-board`: The "Inline add/edit form" requirement gains new behavior for the Due field — `Enter` triggers the picker, and the Due input gets an error highlight CSS class on invalid input.

## Impact

- New widget: `src/knbn/widgets/date_picker.py` — `DateTimePicker` modal screen.
- `src/knbn/widgets/form.py` — Due `Input` intercepts `Enter` key to open the picker; applies error CSS class on validation failure.
- No CSV schema changes. No new third-party dependencies (built with Textual primitives).
