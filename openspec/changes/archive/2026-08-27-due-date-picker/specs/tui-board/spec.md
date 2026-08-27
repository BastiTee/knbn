## MODIFIED Requirements

### Requirement: Inline add/edit form
The TUI SHALL provide an overlay form for creating and editing tasks, accessible via `a` (add) from any view and `Enter` on a focused task from any view (edit). The form SHALL be dismissible with `Esc`. The form SHALL be saveable with `Ctrl+S` provided the title field contains at least one non-whitespace character. The Due field label SHALL read `Due (YYYY-MM-DD or YYYY-MM-DD HH:MM, optional)`. When saving, if the Due field is non-empty and does not match `YYYY-MM-DD` or `YYYY-MM-DD HH:MM`, the form SHALL display an inline validation error below the Due field and SHALL NOT save the task. The Due field SHALL additionally apply a red border highlight (CSS class `--invalid`) when its value fails validation; this highlight SHALL be cleared when the user begins editing the field again.

When `a` is pressed from the Kanban view, the add form SHALL pre-populate the Status and Priority fields based on the currently focused cell: Status from the focused column (`Todo`, `Now`, or `Feedback`) and Priority from the focused swim lane row (`High`, `Medium`, or `Low`). If lane context cannot be determined, the form SHALL fall back to the default values (`Todo` / `Medium`). Pre-populated values SHALL remain editable by the user.

Pressing `Enter` while the Due field is focused SHALL open the `DateTimePicker` overlay instead of submitting the form, subject to the following rules:
- If the Due field is empty, the picker opens with today's date selected and an empty time input.
- If the Due field contains a valid `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` value, the picker opens pre-filled with that value.
- If the Due field contains an invalid value, the validation error is shown (with the `--invalid` highlight) and the picker does NOT open.
On picker confirmation, the returned value is written into the Due field. On picker cancellation, the Due field is unchanged.

#### Scenario: Open add form
- **WHEN** the user presses `a`
- **THEN** an overlay form appears with empty fields ready for input

#### Scenario: Open edit form from any view
- **WHEN** the user presses `Enter` on a focused task in any view
- **THEN** an overlay form appears pre-populated with that task's current field values

#### Scenario: Cancel form with Escape
- **WHEN** the user presses `Esc` while the form is open
- **THEN** the form closes without saving any changes

#### Scenario: Save form with Ctrl+S
- **WHEN** the user presses `Ctrl+S` while the form is open and the title field has at least one character
- **THEN** the task is saved and the form closes

#### Scenario: Ctrl+S ignored when title is empty
- **WHEN** the user presses `Ctrl+S` while the title field is empty or whitespace-only
- **THEN** the form remains open and nothing is saved

#### Scenario: Valid date-only due accepted
- **WHEN** the user enters `2026-08-01` in the Due field and saves
- **THEN** the task is saved with `due = "2026-08-01"`

#### Scenario: Valid datetime due accepted
- **WHEN** the user enters `2026-08-01 09:00` in the Due field and saves
- **THEN** the task is saved with `due = "2026-08-01 09:00"`

#### Scenario: Invalid due format blocked
- **WHEN** the user enters `01/08/2026` in the Due field and attempts to save
- **THEN** an inline error message appears below the Due field and the task is not saved

#### Scenario: Invalid due field gets red border
- **WHEN** validation fails on the Due field (on save attempt or on Enter when invalid)
- **THEN** the Due field border turns red via the `--invalid` CSS class

#### Scenario: Red border cleared on edit
- **WHEN** the user starts typing in the Due field after a validation error
- **THEN** the `--invalid` CSS class is removed and the border returns to normal

#### Scenario: Enter on empty Due field opens picker
- **WHEN** the Due field is empty and the user presses `Enter` while it is focused
- **THEN** the `DateTimePicker` overlay opens with today's date selected

#### Scenario: Enter on valid Due field opens picker pre-filled
- **WHEN** the Due field contains `2026-09-15` and the user presses `Enter` while it is focused
- **THEN** the `DateTimePicker` overlay opens with September 2026 showing and the 15th selected

#### Scenario: Enter on invalid Due field shows error, no picker
- **WHEN** the Due field contains `not-a-date` and the user presses `Enter` while it is focused
- **THEN** the validation error and red border are shown and the picker does NOT open

#### Scenario: Picker confirmation writes value to Due field
- **WHEN** the user confirms a date of `2026-10-01` in the picker
- **THEN** the Due field is updated to `2026-10-01` and the picker closes

#### Scenario: Picker cancellation leaves Due field unchanged
- **WHEN** the user presses `Esc` in the picker
- **THEN** the Due field retains its previous value

#### Scenario: Add form pre-populates status from focused column
- **WHEN** the user is focused on a card or lane header in the `Feedback` column of the Kanban board and presses `a`
- **THEN** the add form opens with Status pre-set to `Feedback`

#### Scenario: Add form pre-populates priority from focused swim lane
- **WHEN** the user is focused on a card or lane header in the `High` swim lane of the Kanban board and presses `a`
- **THEN** the add form opens with Priority pre-set to `High`

#### Scenario: Add form pre-population from focused card
- **WHEN** the user is focused on a card in the `Now` column / `Low` swim lane and presses `a`
- **THEN** the add form opens with Status pre-set to `Now` and Priority pre-set to `Low`

#### Scenario: Add form falls back to defaults when no lane context
- **WHEN** the user presses `a` from the Tabular or Closed view
- **THEN** the add form opens with the default Status (`Todo`) and Priority (`Medium`)
