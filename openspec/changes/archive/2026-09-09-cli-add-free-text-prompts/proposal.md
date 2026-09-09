## Why

`knbn add` captures title, status, priority, category, and key resource — but silently ignores any free-text fields configured in `BoardConfig.free_text_fields`. Tasks added from the CLI always have empty `free_text_1/2/3`, even when those fields carry meaningful labels like "Feedback From" or "Notes".

## What Changes

- After the Key Resource prompt, `knbn add` SHALL prompt for each active free-text field (those with non-empty labels in `BoardConfig.free_text_fields`), using the configured label, skippable with Enter
- Add `--no-free-text` flag to skip all free-text prompts (analogous to `--no-resource`)
- `--fast` / `-f` also skips free-text prompts (in addition to its existing skips)

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `cli-add`: Add free-text field prompts to the `knbn add` command sequence and the `--no-free-text` / `--fast` skip flags

## Impact

- `src/knbn/cli.py`: add `--no-free-text` option, loop over `active_free_text_fields()`, pass `free_text_1/2/3` to Task constructor
- `openspec/specs/cli-add/spec.md`: update `knbn add command` and `Quick-add flags` requirements
