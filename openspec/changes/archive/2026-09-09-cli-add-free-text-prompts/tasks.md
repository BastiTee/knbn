## 1. CLI implementation

- [x] 1.1 In `src/knbn/cli.py`, add `@click.option('--no-free-text', 'no_free_text', is_flag=True, help='Skip free-text field prompts')` and `no_free_text: bool` to the `add` function signature; verify `knbn add --help` shows the new flag
- [x] 1.2 In the `--fast` block, also set `no_free_text = True`; verify `knbn add --fast --title "t"` saves a task with empty free-text fields and shows no free-text prompts
- [x] 1.3 After the Key Resource block, add a loop: for `(i, label)` in `board_config.active_free_text_fields()`, prompt `"<label> (Enter to skip)"` with `default=''` unless `no_free_text`; collect results into a dict keyed by `free_text_1/2/3`
- [x] 1.4 Update the `Task(...)` constructor call to pass `free_text_1`, `free_text_2`, `free_text_3` from the collected values (defaulting to `''`); verify `knbn add` with a configured free-text field saves the entered value in `tasks.csv`

## 2. Tests

- [x] 2.1 In `tests/test_cli.py`, add a test that invokes `knbn add` with active free-text fields configured and verifies the saved task has the prompted values in `free_text_1/2/3`; verify the test passes
- [x] 2.2 Add a test that invokes `knbn add --no-free-text` with active free-text fields configured and verifies all free-text fields are empty string; verify the test passes
- [x] 2.3 Add a test that invokes `knbn add --fast` and verifies no free-text prompts appear and all free-text fields are empty; verify the test passes
