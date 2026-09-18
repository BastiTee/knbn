## Purpose

Modal screen accessible from the command palette that lets users view all configured categories alongside their colors and interactively assign new colors, with save/cancel semantics matching the task editor.

## ADDED Requirements

### Requirement: Command palette entry for category color editor
The system SHALL expose a "Configure Category Colors" entry in the `Ctrl+P` command palette. Selecting it SHALL push the `CategoryColorEditor` modal screen onto the screen stack.

#### Scenario: Command appears in palette
- **WHEN** the user opens the command palette with `Ctrl+P`
- **THEN** a "Configure Category Colors" command is listed

#### Scenario: Selecting the command opens the editor
- **WHEN** the user selects "Configure Category Colors" from the palette
- **THEN** the `CategoryColorEditor` screen is pushed and the palette closes

### Requirement: Category color editor screen layout
The `CategoryColorEditor` SHALL be a `ModalScreen` that displays a scrollable list of all configured categories. Each row SHALL show the category name, a filled color swatch rendered in the category's current color, and the hex value. A **Save** button, a **Scheme** button, and a **Cancel** button SHALL appear at the bottom. While there are unsaved changes the screen title or a status line SHALL indicate the dirty state. A hint line SHALL be visible that describes the available keyboard interactions.

#### Scenario: All categories listed
- **WHEN** the editor opens
- **THEN** every category from the current `BoardConfig` is listed, in config order

#### Scenario: Color swatch shown per row
- **WHEN** the editor opens
- **THEN** each row contains a visual swatch block rendered using the category's hex color

#### Scenario: Hex value shown per row
- **WHEN** the editor opens
- **THEN** each row shows the hex string (e.g. `#4dbfbf`) next to the swatch

#### Scenario: List receives focus on open
- **WHEN** the editor opens
- **THEN** the category list has keyboard focus so the user can navigate immediately without tabbing

#### Scenario: Dirty state indicated
- **WHEN** the user changes one or more category colors without saving
- **THEN** the screen title or a status area shows an unsaved-changes indicator

### Requirement: Color picker overlay
Selecting (clicking or pressing `Enter` on) a category row SHALL open a `ColorPickerOverlay` modal. The overlay SHALL show a focusable palette grid of the ten standard system colors, a live preview swatch reflecting the currently highlighted or typed color, and a hex text input field.

**Palette grid keyboard navigation:** Arrow keys SHALL move a visible cursor through the palette cells; the preview swatch SHALL update live as the cursor moves. Pressing `Enter` on any palette cell SHALL immediately dismiss the overlay and return the selected hex string. Clicking a palette cell SHALL have the same effect.

**Custom hex input:** Tabbing to the hex input allows typing any valid `#rrggbb` value. `Enter` or `Ctrl+S` while the hex input is focused SHALL validate and dismiss the overlay with that value. A "Confirm hex" button SHALL perform the same action.

The overlay SHALL return the chosen hex string on any confirmation path, or `None` on cancellation. The palette grid SHALL receive focus when the overlay opens.

#### Scenario: Palette grid focused on open
- **WHEN** the color picker overlay opens
- **THEN** the palette grid has keyboard focus

#### Scenario: Arrow keys move cursor and update preview
- **WHEN** the palette grid is focused and the user presses an arrow key
- **THEN** the cursor moves to the adjacent palette cell and the preview swatch updates to show that cell's color

#### Scenario: Enter on palette cell selects and closes
- **WHEN** the palette grid is focused and the user presses `Enter`
- **THEN** the overlay closes and returns the color at the current cursor position

#### Scenario: Click on palette cell selects and closes
- **WHEN** the user clicks a palette cell
- **THEN** the overlay closes and returns that cell's color

#### Scenario: Hex input accepts custom color
- **WHEN** the user types a valid 6-digit hex string (e.g. `#a1b2c3`) into the hex input
- **THEN** the live preview swatch updates to reflect that color

#### Scenario: Invalid hex does not update preview
- **WHEN** the user types an incomplete or malformed hex string into the hex input
- **THEN** the preview swatch does not update until the value is a valid `#[0-9a-f]{6}` string

#### Scenario: Confirming hex input updates the row
- **WHEN** the user presses `Enter` or `Ctrl+S` while the hex input is focused, or clicks the Confirm hex button
- **THEN** the overlay closes and the corresponding category row updates its swatch and hex value to the typed color

#### Scenario: Invalid hex blocked on confirm
- **WHEN** the user attempts to confirm with a malformed hex value
- **THEN** an inline error is shown and the overlay remains open

#### Scenario: Cancelling picker leaves row unchanged
- **WHEN** the user cancels the color picker (`Escape`)
- **THEN** the overlay closes and the category row retains its previous color

### Requirement: Color scheme selector
The `CategoryColorEditor` SHALL expose a **Scheme** button and a `Ctrl+T` keyboard binding that opens a `SchemePickerOverlay` modal. The overlay SHALL list ten predefined colour schemes, each shown with its name and a single-row swatch strip of all ten scheme colours. Selecting a scheme SHALL bulk-apply its colours to every category (in list order) as pending changes without saving. Cancelling the overlay SHALL leave pending colours unchanged.

#### Scenario: Scheme picker opened by button
- **WHEN** the user clicks the Scheme button in the editor
- **THEN** the `SchemePickerOverlay` opens

#### Scenario: Scheme picker opened by keyboard
- **WHEN** the user presses `Ctrl+T` while the editor is open
- **THEN** the `SchemePickerOverlay` opens

#### Scenario: Scheme list shows swatch preview
- **WHEN** the scheme picker opens
- **THEN** each row shows the scheme name and a colour swatch strip of the scheme's ten colours

#### Scenario: Scheme list receives focus on open
- **WHEN** the scheme picker opens
- **THEN** the scheme list has keyboard focus

#### Scenario: Selecting a scheme bulk-applies colours
- **WHEN** the user selects a scheme (Enter or click)
- **THEN** all category rows update their swatches and hex values to the scheme colours, and the dirty indicator appears

#### Scenario: Cancelling scheme picker leaves colours unchanged
- **WHEN** the user presses `Escape` in the scheme picker
- **THEN** the overlay closes and no pending colours are changed

### Requirement: Save behavior
Pressing `Ctrl+S` or clicking the **Save** button SHALL persist all pending color changes to `settings.json` (updating the `board.categories` colors), reload the active `BoardConfig`, refresh the running TUI, and dismiss the editor screen.

#### Scenario: Ctrl+S saves and closes
- **WHEN** the user presses `Ctrl+S` while the editor is open
- **THEN** the updated category colors are written to `settings.json`, the board reloads, and the editor screen is dismissed

#### Scenario: Save button saves and closes
- **WHEN** the user clicks the Save button
- **THEN** the updated category colors are written to `settings.json`, the board reloads, and the editor screen is dismissed

#### Scenario: Colors are immediately reflected in the running TUI
- **WHEN** the editor is saved
- **THEN** the running TUI (kanban board and other views) uses the new category colors without restarting

### Requirement: Cancel behavior
Pressing `Escape` or clicking the **Cancel** button SHALL discard all pending color changes and dismiss the editor without modifying `settings.json`.

#### Scenario: Escape discards changes
- **WHEN** the user presses `Escape` while the editor is open
- **THEN** the editor is dismissed and `settings.json` is not modified

#### Scenario: Cancel button discards changes
- **WHEN** the user clicks the Cancel button
- **THEN** the editor is dismissed and `settings.json` is not modified

#### Scenario: No reload on cancel
- **WHEN** the user cancels the editor after changing one or more colors
- **THEN** the running TUI retains the colors that were active before the editor was opened

