# date-time-picker

## Purpose

Modal overlay widget providing calendar-based date selection and optional time input, used wherever a date/time value needs to be entered or edited in the TUI.

## Requirements

### Requirement: Date/time picker overlay
The system SHALL provide a `DateTimePicker` modal overlay that presents a calendar month grid and an optional time input row. It SHALL accept an optional pre-fill value (`YYYY-MM-DD` or `YYYY-MM-DD HH:MM`). On confirmation it SHALL return the selected value as a string in `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` format. On cancellation it SHALL return `None`. The calendar SHALL display the full month of the selected or current date, with day cells arranged in a standard Mon–Sun weekly grid. The current month and year SHALL be shown in a header row. Today's date SHALL be visually distinguished. The selected date SHALL be visually distinguished from today and from unselected days.

#### Scenario: Opens at today when no pre-fill
- **WHEN** the picker is opened with no pre-fill value
- **THEN** the calendar shows the current month and today's date is selected

#### Scenario: Opens pre-filled with existing date
- **WHEN** the picker is opened with a valid `YYYY-MM-DD` value
- **THEN** the calendar navigates to that month and highlights the corresponding day

#### Scenario: Opens pre-filled with existing datetime
- **WHEN** the picker is opened with a valid `YYYY-MM-DD HH:MM` value
- **THEN** the calendar highlights the date and the time input is pre-filled with `HH:MM`

#### Scenario: Today highlighted distinctly
- **WHEN** the current date is visible in the calendar
- **THEN** today's cell is rendered with a distinct background or border

#### Scenario: Selected date highlighted
- **WHEN** a date is selected
- **THEN** its cell is rendered with a distinct accent colour different from today's highlight

### Requirement: Date/time picker keyboard navigation
The picker SHALL support fully keyboard-driven interaction using only keys already available in the broader application. Left/right arrow keys SHALL move the selection one day backward/forward and SHALL wrap automatically to the previous/next month when crossing a month boundary. Up/down arrow keys SHALL move the selection one week backward/forward and SHALL wrap months as needed. `Enter` SHALL confirm the current selection and close the picker. `Esc` SHALL cancel without changing the Due field. `Tab` SHALL move focus from the calendar to the time input row; `Shift+Tab` SHALL move focus back.

#### Scenario: Left arrow moves to previous day
- **WHEN** the calendar is focused and the user presses `←`
- **THEN** the selection moves to the day before the currently selected day

#### Scenario: Right arrow moves to next day
- **WHEN** the calendar is focused and the user presses `→`
- **THEN** the selection moves to the day after the currently selected day

#### Scenario: Up arrow moves one week back
- **WHEN** the calendar is focused and the user presses `↑`
- **THEN** the selection moves 7 days earlier

#### Scenario: Down arrow moves one week forward
- **WHEN** the calendar is focused and the user presses `↓`
- **THEN** the selection moves 7 days later

#### Scenario: Left arrow at month start wraps to previous month
- **WHEN** the first day of the month is selected and the user presses `←`
- **THEN** the calendar navigates to the previous month and selects its last day

#### Scenario: Right arrow at month end wraps to next month
- **WHEN** the last day of the month is selected and the user presses `→`
- **THEN** the calendar navigates to the next month and selects its first day

#### Scenario: Enter confirms date-only selection
- **WHEN** the calendar is focused and the user presses `Enter` with the time input empty
- **THEN** the picker closes and returns the selected date in `YYYY-MM-DD` format

#### Scenario: Enter confirms datetime selection
- **WHEN** the time input contains a valid `HH:MM` value and the user presses `Enter`
- **THEN** the picker closes and returns `YYYY-MM-DD HH:MM`

#### Scenario: Esc cancels picker
- **WHEN** the user presses `Esc`
- **THEN** the picker closes and returns `None` without modifying the Due field

#### Scenario: Tab moves focus to time input
- **WHEN** the calendar is focused and the user presses `Tab`
- **THEN** focus moves to the time input row

### Requirement: Date/time picker time input
The time input row SHALL contain a single text field accepting `HH:MM` format (24-hour). The field SHALL be optional — leaving it empty results in a date-only return value. When the time input is focused, up/down arrows SHALL increment/decrement the value at the cursor position: up/down when the cursor is on the hour digits SHALL adjust the hour by 1 (clamped to 00–23); when on the minute digits SHALL adjust the minute by 1 (clamped to 00–59). On confirmation, if the time input is non-empty and does not match `HH:MM` (two-digit hour 00–23, two-digit minute 00–59), the picker SHALL display an inline error and SHALL NOT close.

#### Scenario: Empty time input returns date-only
- **WHEN** the user confirms with the time input empty
- **THEN** the picker returns `YYYY-MM-DD` with no time component

#### Scenario: Valid time input returns datetime
- **WHEN** the user enters `14:30` in the time input and confirms
- **THEN** the picker returns `YYYY-MM-DD 14:30`

#### Scenario: Invalid time blocked on confirm
- **WHEN** the user enters `25:00` in the time input and presses `Enter`
- **THEN** an inline error is shown and the picker remains open

#### Scenario: Up arrow increments hour
- **WHEN** the cursor is positioned on the hour digits and the user presses `↑`
- **THEN** the hour value increments by 1, wrapping from 23 to 00

#### Scenario: Down arrow decrements minute
- **WHEN** the cursor is positioned on the minute digits and the user presses `↓`
- **THEN** the minute value decrements by 1, wrapping from 00 to 59

### Requirement: Date/time picker mouse support
Calendar day cells SHALL be clickable. A single click on a day cell SHALL select that date. A double-click SHALL select the date and confirm (equivalent to click + Enter). The time input row SHALL be mouse-focusable.

#### Scenario: Click selects a day
- **WHEN** the user clicks a day cell
- **THEN** that day becomes the selected date

#### Scenario: Double-click confirms date
- **WHEN** the user double-clicks a day cell
- **THEN** the picker closes with that date selected (date-only, unless time input is filled)
