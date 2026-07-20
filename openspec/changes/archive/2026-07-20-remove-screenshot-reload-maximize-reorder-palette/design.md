## Context

`KnbnApp` inherits from Textual's `App`, which provides built-in system commands (Screenshot, Maximize/Minimize, Theme, Quit, Keys) surfaced via `ctrl+p`. The default `get_system_commands` yields them in a fixed order. `KnbnApp` also has an `r Reload` binding that re-reads the CSV and redraws the kanban view — redundant because every mutation already calls `_reload_tasks` and every view switch also reloads.

## Goals / Non-Goals

**Goals:**
- Remove `r Reload` from the footer and the help overlay.
- Remove Screenshot and Maximize/Minimize from the `ctrl+p` palette.
- Ensure Quit appears directly below Theme in the palette (Theme → Quit → Keys).

**Non-Goals:**
- Removing `ctrl+p` or the command palette itself.
- Changing any other keybinding or command.

## Decisions

**Override `get_system_commands` rather than disabling the palette.**  
`ENABLE_COMMAND_PALETTE = False` would remove the whole palette. We only want to filter three commands, so a targeted override of `get_system_commands` that yields `Theme → Quit → Keys` (omitting Screenshot and Maximize) is the minimal, idiomatic approach.

**Keep `_reload_tasks` as a private helper — just remove the public `action_reload` and its binding.**  
`_reload_tasks` is still called on mount, view switch, and after mutations. Only the publicly-triggered action is removed.

## Risks / Trade-offs

- No risks. All changes are subtractive — no new behaviour, no data model impact.
