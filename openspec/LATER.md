# Later / Deferred Ideas

## Migrate TUI from index-based to ID-based store operations

Once the `agent-cli` change lands, the store will have both index-based
(`update_task`, `delete_task`) and ID-based (`update_task_by_id`,
`delete_task_by_id`) CRUD functions. The TUI still uses the index-based
ones — it loads the task list, the user picks a row, and the row number
is used as the lookup key.

The follow-up work is to thread each task's `id` field through the TUI
widget state (currently just a list index) and switch the app to call the
ID-based functions instead. Once that is done the index-based functions
can be removed from the store.

Deferred because: it's a non-trivial TUI refactor with no user-visible
change, and the index-based path is correct as long as the TUI holds an
exclusive view of the list (which it does).
