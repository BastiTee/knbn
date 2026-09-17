## MODIFIED Requirements

### Requirement: Swim lane collapsibility
Each (column × priority) cell of the Kanban board SHALL be independently collapsible. Toggling a lane header SHALL only affect the single cell it belongs to — collapsing or expanding cards in that specific column for that specific priority. Lanes with the same priority in other columns SHALL NOT be affected. A collapsed lane SHALL show only the lane header; all cards in that lane SHALL be hidden.

#### Scenario: Collapse swim lane in one column only
- **WHEN** the user presses Enter on a focused lane header in the `Todo` column for priority `Medium`
- **THEN** only the `Medium` lane in `Todo` collapses; the `Medium` lanes in `Now` and `Feedback` remain unchanged

#### Scenario: Expand swim lane in one column only
- **WHEN** a collapsed lane header in the `Now` column for priority `High` is focused and the user presses Enter
- **THEN** only the `High` lane in `Now` expands; other columns are unaffected

#### Scenario: Independent collapse state per cell
- **WHEN** the `High` lane is collapsed in `Todo` and expanded in `Now`
- **THEN** both states are preserved simultaneously and reflected correctly in each column

#### Scenario: Collapse hides cards in that cell
- **WHEN** a lane is collapsed
- **THEN** all task cards in that (column × priority) cell are hidden and only the header is visible

#### Scenario: Expand restores cards in that cell
- **WHEN** a collapsed lane is expanded
- **THEN** all task cards in that (column × priority) cell become visible again
