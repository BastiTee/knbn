# db-version

## Purpose

Records the knbn version that last mutated the data store in settings.json, enabling future migrations to detect which transformations need to be applied to older stores.

## Requirements

### Requirement: db_version key in settings.json
The system SHALL write a `db_version` key at the top level of `settings.json` whenever it creates or migrates the data store. The value SHALL be the current knbn package version string (e.g. `"0.3.0"`). The key SHALL be absent from stores that have never been initialized or migrated by a version that supports this field.

#### Scenario: db_version written on store init
- **WHEN** `ensure_data_dir` initializes a new data directory
- **THEN** `settings.json` contains `"db_version": "<current_version>"`

#### Scenario: db_version updated after migration
- **WHEN** `save_tasks` performs a backward-compatible ID migration
- **THEN** `settings.json` is updated with the current `db_version`

#### Scenario: Legacy store missing db_version is valid
- **WHEN** `settings.json` exists but has no `db_version` key
- **THEN** the store loads without error and the absence of `db_version` is treated as a pre-ID-migration store

### Requirement: Version source
The `db_version` value SHALL be read from the installed package metadata at runtime (e.g. `importlib.metadata.version("knbn")`), not hardcoded.

#### Scenario: db_version matches installed package version
- **WHEN** `settings.json` is written during store initialization
- **THEN** the `db_version` string matches the output of `importlib.metadata.version("knbn")`
