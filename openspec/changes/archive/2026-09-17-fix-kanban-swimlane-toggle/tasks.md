## 1. Extend LaneHeader

- [x] 1.1 Add `status: str` parameter to `LaneHeader.__init__`, store as `self._status`, and add `status` field to `LaneHeader.Toggled`; verify the class compiles without type errors (`uv run mypy src/`)
- [x] 1.2 Update `LaneHeader.on_key` to include `self._status` in the posted `Toggled` message; verify no regressions by running `uv run pytest tests`

## 2. Scope collapse state to (status, priority) cells

- [x] 2.1 Change `KanbanView._collapsed` from `set[str]` to `set[tuple[str, str]]` and update `compose()` to check `(status, priority)` membership; verify the board still renders and `uv run mypy src/` passes
- [x] 2.2 Update `on_lane_header_toggled` to add/discard `(message.status, message.priority)` and restrict DOM mutation to only the column matching `message.status`; verify `uv run pytest tests` is green

## 3. Pass status at construction

- [x] 3.1 Update all `LaneHeader(...)` instantiation sites in `KanbanView.compose()` to pass the current `status` argument; verify `uv run mypy src/` and `uv run pytest tests` both pass

## 4. Verify behaviour end-to-end

- [ ] 4.1 Run `uv run knbn board` with demo data and confirm that collapsing a lane in one column leaves the same-priority lanes in other columns unaffected; confirm expand works symmetrically
- [x] 4.2 Run the full build chain (`make build`) and confirm it exits clean
