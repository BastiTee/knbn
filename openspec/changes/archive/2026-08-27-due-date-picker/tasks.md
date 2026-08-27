## 1. DateTimePicker widget — calendar grid

- [x] 1.1 Create `src/knbn/widgets/date_picker.py` with a `_CalendarGrid` widget that renders a Mon–Sun 7-column month grid, highlights today and the selected day, and tracks the currently selected date
- [x] 1.2 Implement left/right arrow navigation (day ±1, with month wrap) and up/down arrow navigation (week ±7, with month wrap) on `_CalendarGrid`
- [x] 1.3 Add mouse click support on day cells: single click selects the day, double-click selects and posts a confirm message

## 2. DateTimePicker widget — time input and modal wiring

- [x] 2.1 Add a `HH:MM` `Input` row below the calendar; pre-fill it when the picker is opened with a datetime value
- [x] 2.2 Implement up/down arrow increment/decrement on hour and minute digits when the time input is focused (detect cursor position to determine hour vs minute)
- [x] 2.3 Implement `Enter` to confirm: validate the time input (if non-empty), show inline error on invalid, otherwise dismiss with the formatted date string
- [x] 2.4 Implement `Esc` to cancel (dismiss with `None`) and `Tab`/`Shift+Tab` to move focus between calendar and time input
- [x] 2.5 Create `DateTimePicker(ModalScreen[str | None])` that composes `_CalendarGrid` + time input, accepts an optional pre-fill string, and positions itself centred on screen

## 3. DueInput subclass and form wiring

- [x] 3.1 Create `DueInput(Input)` in `form.py` with a `DueInput.OpenPicker` message; override `_on_key` to post it instead of the default `Enter` behaviour
- [x] 3.2 Replace the Due `Input` in `TaskForm.compose()` with `DueInput`
- [x] 3.3 Add `--invalid` CSS class to `DueInput` styling (`border: tall $error`) and apply/remove the class on validation failure and on `Input.Changed` respectively
- [x] 3.4 Handle `DueInput.EnterPressed` in `TaskForm`: validate the field value, show error + `--invalid` on invalid, open `DateTimePicker` pre-filled on valid/empty; write the picker return value back into the field on confirmation

## 4. Validation and test coverage

- [x] 4.1 Ensure the existing `_DUE_RE` validation path also applies the `--invalid` class when a save is attempted with a bad value
- [x] 4.2 Add unit tests for `_CalendarGrid` navigation logic (day/week advance, month wrap) and time-increment helpers in isolation
