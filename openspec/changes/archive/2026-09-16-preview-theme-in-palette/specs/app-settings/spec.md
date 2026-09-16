## MODIFIED Requirements

### Requirement: Theme setting
The system SHALL support a `theme` setting under the `app` block whose value is any Textual theme name. The default value SHALL be `textual-dark`. The TUI SHALL read `settings["app"]["theme"]` on startup and apply the corresponding Textual theme.

The theme picker SHALL be presented as a sidebar docked to the right edge of the window (bounded to roughly a third of the window's width), not as a centered overlay covering most of the screen. The rest of the board SHALL remain visible behind the sidebar while it is open.

While the theme sidebar is open, highlighting a theme (moving the selection cursor without confirming) SHALL apply that theme live to the running app for preview purposes only, and SHALL NOT write it to `settings.json`. Confirming a highlighted theme (selecting it) SHALL apply it and persist it to `settings.json`, replacing the previously saved value. Closing the sidebar without confirming a selection SHALL revert the app's active theme to whichever theme was active immediately before the sidebar was opened, and SHALL leave `settings.json` unchanged.

#### Scenario: Default theme is textual-dark
- **WHEN** no `settings.json` exists or the `app.theme` key is absent
- **THEN** the TUI launches with the `textual-dark` theme

#### Scenario: Alternative theme applied
- **WHEN** `settings.json` contains `{"app": {"theme": "nord"}}`
- **THEN** the TUI launches with the `nord` theme

#### Scenario: Theme sidebar does not obscure the board
- **WHEN** the theme sidebar is open
- **THEN** it occupies a bounded strip docked to the right edge of the window
- **AND** the rest of the board remains visible behind it

#### Scenario: Highlighting a theme previews it without persisting
- **WHEN** the theme sidebar is open and the user moves the selection to highlight a different theme, without confirming
- **THEN** the app's active theme changes to the highlighted theme
- **AND** `settings.json` is not modified

#### Scenario: Confirming a highlighted theme persists it
- **WHEN** the theme sidebar is open, a theme is highlighted, and the user confirms the selection
- **THEN** the app's active theme is the confirmed theme
- **AND** `settings.json` is updated to store that theme

#### Scenario: Cancelling the sidebar reverts the preview
- **WHEN** the theme sidebar is open, the user highlights one or more themes without confirming, and then closes the sidebar without selecting one
- **THEN** the app's active theme reverts to the theme that was active before the sidebar was opened
- **AND** `settings.json` remains unchanged
