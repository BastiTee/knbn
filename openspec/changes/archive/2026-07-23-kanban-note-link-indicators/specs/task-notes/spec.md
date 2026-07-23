## MODIFIED Requirements

### Requirement: Notes presence indicator on card
Each task card SHALL display a visual indicator when metadata is present:
- `☰` when a Markdown notes file exists for that task
- `※` when the task has a `key_resource` URL set
- `☰ ※` (space-separated) when both are present
- No indicator when neither is present

The indicator SHALL be appended to the title line with a single leading space.

#### Scenario: Notes indicator shown when notes exist and no link
- **WHEN** a task has a corresponding notes file in `notes/` and no `key_resource` set
- **THEN** the task card displays `☰` after the title

#### Scenario: Link indicator shown when key_resource set and no notes
- **WHEN** a task has a `key_resource` URL and no corresponding notes file
- **THEN** the task card displays `※` after the title

#### Scenario: Both indicators shown when notes and link present
- **WHEN** a task has both a corresponding notes file and a `key_resource` URL
- **THEN** the task card displays `☰ ※` after the title (notes first, link second)

#### Scenario: No indicator when neither notes nor link present
- **WHEN** a task has no corresponding notes file and no `key_resource`
- **THEN** the task card displays no indicator after the title

#### Scenario: Indicator shown when notes exist
- **WHEN** a task has a corresponding notes file in `notes/`
- **THEN** the task card displays the notes indicator `☰`

#### Scenario: No indicator when notes absent
- **WHEN** a task has no corresponding notes file and no `key_resource`
- **THEN** the task card displays no notes indicator
