## ADDED Requirements

### Requirement: Board config save helper
The system SHALL provide a `save_board_config(data_dir, board_config)` function that serialises a `BoardConfig` back to the `board` block of `settings.json` atomically, preserving the `app` block unchanged. The function SHALL load the current settings via `load_settings`, replace the `board` key with the serialised `BoardConfig`, and write the merged dict back via `save_settings`.

#### Scenario: Board block updated, app block preserved
- **WHEN** `save_board_config(data_dir, updated_config)` is called
- **THEN** `settings.json` contains the updated `board` values and the `app` block is unchanged

#### Scenario: Write is atomic
- **WHEN** `save_board_config` is called
- **THEN** the write goes through `save_settings` and is therefore atomic (tmp-rename)

#### Scenario: Updated colors round-trip correctly
- **WHEN** `save_board_config` is called with a `BoardConfig` where one category's color has changed
- **THEN** `load_board_config()` on the same `data_dir` afterwards returns a `BoardConfig` with that updated color
