## MODIFIED Requirements

### Requirement: db_version key in settings.json
The system SHALL write a `db_version` key at the top level of `settings.json` whenever it creates, migrates, or accesses the data store via any CLI command or TUI launch. The value SHALL be the current knbn package version string (e.g. `"0.3.0"`). The key SHALL be absent from stores that have never been initialized or accessed by a version that supports this field. After any knbn command that resolves the data directory, the `db_version` in `settings.json` SHALL reflect the currently installed package version.

#### Scenario: db_version written on store init
- **WHEN** `ensure_data_dir` initializes a new data directory
- **THEN** `settings.json` contains `"db_version": "<current_version>"`

#### Scenario: db_version updated after migration
- **WHEN** `save_tasks` performs a backward-compatible ID migration
- **THEN** `settings.json` is updated with the current `db_version`

#### Scenario: db_version refreshed on read-only commands
- **WHEN** a read-only command (e.g. `knbn config`, `knbn list`) is executed against an existing data directory whose `db_version` is behind the installed version
- **THEN** `settings.json` is updated so `db_version` equals the installed version before the command output is produced

#### Scenario: Legacy store missing db_version is valid
- **WHEN** `settings.json` exists but has no `db_version` key
- **THEN** the store loads without error and the absence of `db_version` is treated as a pre-ID-migration store
