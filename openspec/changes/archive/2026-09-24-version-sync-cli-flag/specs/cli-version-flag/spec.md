## Purpose

Exposes the installed knbn package version through the CLI so users can quickly verify which release is running without inspecting package metadata manually.

## ADDED Requirements

### Requirement: --version flag on root command
The `knbn` CLI SHALL accept a `--version` (short: `-V`) flag on the root command group. When the flag is present, the CLI SHALL print the installed package version string and exit with code 0. No subcommand is required; the flag works even when invoked as `knbn --version` without any subcommand.

#### Scenario: Version output format
- **WHEN** the user runs `knbn --version`
- **THEN** the CLI prints `knbn, version <X.Y.Z>` (where `<X.Y.Z>` is the installed version) to stdout and exits with code 0

#### Scenario: Short flag -V works identically
- **WHEN** the user runs `knbn -V`
- **THEN** the output and exit code are identical to `knbn --version`

#### Scenario: Version source matches package metadata
- **WHEN** the `--version` flag is evaluated
- **THEN** the version string matches `importlib.metadata.version("knbn")`

#### Scenario: --version takes precedence over subcommands
- **WHEN** the user runs `knbn --version board`
- **THEN** the CLI prints the version and exits without launching the board
