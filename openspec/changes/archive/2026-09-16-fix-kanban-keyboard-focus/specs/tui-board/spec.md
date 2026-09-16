## ADDED Requirements

### Requirement: Focus restoration after board mutations
After any action that removes a widget from the Kanban board (lane toggle, task deletion, mark-done), the board SHALL restore keyboard focus to a well-defined element without requiring the user to press Tab or any other key.

**Lane toggle**: After the user presses Enter to collapse or expand a lane header, that same lane header SHALL remain focused after the board recomposes.

**Task deletion**: After the user confirms deletion of a task, focus SHALL land on the next card below the deleted card within the same column (counting from the top of the column, ignoring swimlane boundaries). If no card exists below, focus SHALL land on the card above. If the column has no remaining cards, focus SHALL land on the topmost visible `LaneHeader` in that column.

**Mark-done**: After the user confirms the mark-done action, focus SHALL land using the same rule as task deletion.

#### Scenario: Focus stays on lane header after collapse
- **WHEN** the user presses Enter on a focused lane header to collapse it
- **THEN** the same lane header retains focus after the board recomposes

#### Scenario: Focus stays on lane header after expand
- **WHEN** the user presses Enter on a collapsed lane header to expand it
- **THEN** the same lane header retains focus after the board recomposes

#### Scenario: Focus moves to next card after delete
- **WHEN** the user confirms deletion of a task that has another card below it in the same column
- **THEN** the card that was directly below the deleted card receives focus after the board recomposes

#### Scenario: Focus moves to previous card when last card deleted
- **WHEN** the user confirms deletion of the last card in a column (no cards below, one card above)
- **THEN** the card above the deleted card receives focus after the board recomposes

#### Scenario: Focus moves to lane header when last card in column deleted
- **WHEN** the user confirms deletion of the only remaining card in a column
- **THEN** the topmost visible lane header in that column receives focus after the board recomposes

#### Scenario: Focus moves to next card after mark-done
- **WHEN** the user confirms mark-done on a task that has another card below it in the same column
- **THEN** the card that was directly below the completed task receives focus after the board recomposes

#### Scenario: Focus moves to previous card when last card marked done
- **WHEN** the user confirms mark-done on the last card in a column (no cards below, one card above)
- **THEN** the card above receives focus after the board recomposes

#### Scenario: Focus moves to lane header when only card marked done
- **WHEN** the user confirms mark-done on the only remaining card in a column
- **THEN** the topmost visible lane header in that column receives focus after the board recomposes
