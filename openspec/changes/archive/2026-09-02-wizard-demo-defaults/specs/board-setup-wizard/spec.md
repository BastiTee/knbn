## ADDED Requirements

### Requirement: Quick-start prompt
The wizard SHALL display a quick-start prompt as its **first step**, before any individual configuration steps: "Use standard settings? [Y/n]". Pressing Enter or `y` accepts; pressing `n` declines. If the user accepts, the wizard SHALL call `load_default_board_config()` from `knbn.config`, write the returned dict as the `board` block of `settings.json`, print a confirmation line, and return without executing any further wizard steps.

#### Scenario: User accepts quick-start defaults
- **WHEN** the wizard starts and the user presses Enter (or `y`) at the quick-start prompt
- **THEN** the wizard writes the default board config to `settings.json`, prints a confirmation, and exits without presenting any further prompts

#### Scenario: User declines quick-start defaults
- **WHEN** the user types `n` at the quick-start prompt
- **THEN** the wizard proceeds to the active status configuration step as normal

#### Scenario: Quick-start is the first thing shown
- **WHEN** the wizard is triggered on a blank-slate install
- **THEN** the quick-start prompt appears before any status, priority, category, or free-text prompts
