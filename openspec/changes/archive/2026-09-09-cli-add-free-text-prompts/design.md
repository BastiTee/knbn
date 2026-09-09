## Context

`knbn add` builds a `Task` and calls `add_task()`. The `Task` dataclass has `free_text_1`, `free_text_2`, `free_text_3` fields (all default to `''`). The CLI currently never prompts for them and always passes the defaults.

`BoardConfig.active_free_text_fields()` returns `[(index, label)]` pairs for non-empty slots only — this is exactly the loop driver needed.

The Key Resource prompt pattern is the model:
```python
raw = click.prompt(label + ' (Enter to skip)', default='')
value = '' if raw in ('', '-') else raw
```

See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Prompt for each active free-text field after Key Resource, using its configured label
- Add `--no-free-text` flag to skip all free-text prompts
- `--fast` implies `--no-free-text`

**Non-Goals:**
- Validation of free-text content (any string including empty is valid)
- TUI form changes (out of scope)
- Changing the Task dataclass or CSV schema

## Decisions

**Loop over `active_free_text_fields()`** — returns only non-empty-label slots in index order; no special-casing needed for partially configured boards.

**Map index to field name with `f'free_text_{i+1}'`** — indices 0/1/2 map to `free_text_1/2/3`; construct the Task with `**kwargs` or use a dict-based approach since Task is a dataclass.

**`--no-free-text` mirrors `--no-resource`** — same pattern: bool flag, skips the prompts, stores empty strings. `--fast` sets both `no_resource = no_free_text = True`.

**Prompt label**: `"<Label> (Enter to skip)"` — consistent with Key Resource.

## Risks / Trade-offs

- [Board with no active free-text fields] → Loop body never executes; no UX change for existing users.
- [--fast changes meaning] → `--fast` now additionally implies `--no-free-text`. This is additive and consistent with its existing "skip all optional prompts" contract.
