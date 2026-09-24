"""Tests for CLI commands."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from knbn.cli import add, config, delete, edit, init, list_tasks
from knbn.model.store import add_task, ensure_data_dir
from knbn.model.task import Task


@pytest.fixture()
def data_dir(tmp_path: Path) -> Path:
    return tmp_path / 'knbn'


def test_init_creates_data_dir(data_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.setup.should_run_wizard', return_value=False):
        result = runner.invoke(init)
    assert result.exit_code == 0
    assert data_dir.is_dir()
    assert (data_dir / 'tasks.csv').exists()
    assert (data_dir / 'notes').is_dir()
    assert 'Initialized' in result.output


def test_init_idempotent(data_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.setup.should_run_wizard', return_value=False):
        runner.invoke(init)
        result = runner.invoke(init)
    assert result.exit_code == 0
    assert 'Already initialized' in result.output


def test_init_with_explicit_path(tmp_path: Path) -> None:
    target = tmp_path / 'custom'
    runner = CliRunner()
    with patch('knbn.setup.should_run_wizard', return_value=False):
        result = runner.invoke(init, [str(target)])
    assert result.exit_code == 0
    assert target.is_dir()


def test_init_runs_wizard_on_blank_slate(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    wizard_called = []

    def fake_wizard(d: Path) -> None:
        wizard_called.append(d)

    with (
        patch('knbn.setup.should_run_wizard', return_value=True),
        patch('knbn.setup.run_setup_wizard', side_effect=fake_wizard),
    ):
        result = runner.invoke(init)
    assert result.exit_code == 0
    assert len(wizard_called) == 1


def test_init_skips_wizard_when_tasks_exist(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.setup.should_run_wizard', return_value=False) as mock_check:
        runner.invoke(init)
    mock_check.assert_called()


def test_add_fast_with_title(data_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(add, ['--fast', '--title', 'My fast task'])
    assert result.exit_code == 0
    assert '✓ Task added: My fast task' in result.output
    mock_add.assert_called_once()
    task: Task = mock_add.call_args[0][1]
    assert task.title == 'My fast task'
    assert task.status == 'Todo'
    assert task.priority == 'Medium'
    assert task.category == 'Other'
    assert task.key_resource == ''


def test_add_fast_flag_short_form(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.cli.add_task'):
        result = runner.invoke(add, ['-f', '--title', 'Quick task'])
    assert result.exit_code == 0


def test_add_prompts_title_when_not_provided(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.cli.add_task'):
        result = runner.invoke(add, ['--fast'], input='Prompted title\n')
    assert result.exit_code == 0
    assert '✓ Task added: Prompted title' in result.output


def test_add_status_default_flag(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(
            add,
            [
                '--title',
                'Task',
                '--status-default',
                '--priority-default',
                '--category-default',
                '--no-resource',
                '--no-free-text',
            ],
        )
    assert result.exit_code == 0
    task: Task = mock_add.call_args[0][1]
    assert task.status == 'Todo'


def test_add_stores_dates(data_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.cli.add_task') as mock_add:
        runner.invoke(add, ['--fast', '--title', 'Dated task'])
    task: Task = mock_add.call_args[0][1]
    assert task.date_created != ''
    assert task.date_modified != ''
    assert task.date_created == task.date_modified


def test_add_interactive_prompts_full(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test add with all prompts answered interactively (no flags)."""
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    # Inputs: title, status (1=Todo), priority (1=High), category (1=Personal), resource (empty),
    # free_text_1 (Feedback From, skip), free_text_2 (Delegated To, skip)
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(add, [], input='Interactive task\n1\n1\n1\n\n\n\n')
    assert result.exit_code == 0
    assert '✓ Task added: Interactive task' in result.output
    task: Task = mock_add.call_args[0][1]
    assert task.title == 'Interactive task'
    assert task.status == 'Todo'
    assert task.priority == 'High'
    assert task.category == 'Personal'
    assert task.key_resource == ''


def test_add_no_free_text_fields_in_cli(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """--fast implies --no-free-text; free-text fields are empty."""
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(add, ['--fast', '--title', 'Plain task'])
    assert result.exit_code == 0
    task: Task = mock_add.call_args[0][1]
    assert task.free_text_1 == ''
    assert task.free_text_2 == ''
    assert task.free_text_3 == ''


def test_add_with_key_resource(data_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(
            add,
            [
                '--title',
                'Resource task',
                '--status-default',
                '--priority-default',
                '--category-default',
                '--no-free-text',
            ],
            input='https://example.com/thread\n',
        )
    assert result.exit_code == 0
    task: Task = mock_add.call_args[0][1]
    assert task.key_resource == 'https://example.com/thread'


def test_add_dash_clears_resource(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(
            add,
            [
                '--title',
                'No link',
                '--status-default',
                '--priority-default',
                '--category-default',
                '--no-free-text',
            ],
            input='-\n',
        )
    assert result.exit_code == 0
    task: Task = mock_add.call_args[0][1]
    assert task.key_resource == ''


def test_add_free_text_prompts_with_active_fields(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Free-text prompts appear for each active field; entered values are saved."""
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    # Default config has Feedback From (idx 0) and Delegated To (idx 1) active
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(
            add,
            [
                '--title',
                'FT task',
                '--status-default',
                '--priority-default',
                '--category-default',
                '--no-resource',
            ],
            input='Alice\nBob\n',
        )
    assert result.exit_code == 0
    task: Task = mock_add.call_args[0][1]
    assert task.free_text_1 == 'Alice'
    assert task.free_text_2 == 'Bob'
    assert task.free_text_3 == ''


def test_add_no_free_text_flag_skips_prompts(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """--no-free-text skips all free-text prompts; fields are empty string."""
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(
            add,
            [
                '--title',
                'No FT',
                '--status-default',
                '--priority-default',
                '--category-default',
                '--no-resource',
                '--no-free-text',
            ],
        )
    assert result.exit_code == 0
    task: Task = mock_add.call_args[0][1]
    assert task.free_text_1 == ''
    assert task.free_text_2 == ''
    assert task.free_text_3 == ''


def test_add_fast_skips_free_text_prompts(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """--fast implies --no-free-text; no free-text prompts appear."""
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(add, ['--fast', '--title', 'Fast task'])
    assert result.exit_code == 0
    assert 'Feedback From' not in result.output
    assert 'Delegated To' not in result.output
    task: Task = mock_add.call_args[0][1]
    assert task.free_text_1 == ''
    assert task.free_text_2 == ''


def _make_task(**kwargs: str) -> Task:
    defaults: dict[str, str] = {
        'title': 'Test task',
        'category': 'Ideas',
        'status': 'Todo',
        'priority': 'Medium',
        'date_created': '2026-07-01 14:27',
        'date_modified': '2026-07-01 14:27',
    }
    defaults.update(kwargs)
    return Task(**defaults)


# --- add --json ---


def test_add_json_returns_task_with_id(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    result = runner.invoke(add, ['--fast', '--title', 'JSON task', '--json'])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload['title'] == 'JSON task'
    assert payload['id']
    assert len(payload['id']) == 8


def test_add_json_has_all_fields(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    result = runner.invoke(add, ['--fast', '--title', 'T', '--json'])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    for field_name in [
        'id',
        'title',
        'status',
        'priority',
        'category',
        'due',
        'key_resource',
        'free_text_1',
        'free_text_2',
        'free_text_3',
        'date_created',
        'date_modified',
    ]:
        assert field_name in payload


# --- list ---


def test_list_shows_active_tasks(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    add_task(data_dir, _make_task(title='Active', status='Todo'))
    add_task(data_dir, _make_task(title='Done task', status='Done'))
    runner = CliRunner()
    result = runner.invoke(list_tasks, [])
    assert result.exit_code == 0
    assert 'Active' in result.output
    assert 'Done task' not in result.output


def test_list_all_includes_terminal_tasks(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    add_task(data_dir, _make_task(title='Done task', status='Done'))
    runner = CliRunner()
    result = runner.invoke(list_tasks, ['--all'])
    assert result.exit_code == 0
    assert 'Done task' in result.output


def test_list_json_returns_array(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    add_task(data_dir, _make_task(title='Task 1'))
    add_task(data_dir, _make_task(title='Task 2'))
    runner = CliRunner()
    result = runner.invoke(list_tasks, ['--json'])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert isinstance(payload, list)
    assert len(payload) == 2
    assert all('id' in t for t in payload)


def test_list_json_empty_result(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    runner = CliRunner()
    result = runner.invoke(list_tasks, ['--status', 'Now', '--json'])
    assert result.exit_code == 0
    assert json.loads(result.output) == []


def test_list_filter_by_status(data_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    add_task(data_dir, _make_task(title='Now task', status='Now'))
    add_task(data_dir, _make_task(title='Todo task', status='Todo'))
    runner = CliRunner()
    result = runner.invoke(list_tasks, ['--status', 'Now', '--json'])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert len(payload) == 1
    assert payload[0]['title'] == 'Now task'


def test_list_filter_repeatable_is_union(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    add_task(data_dir, _make_task(title='Now task', status='Now'))
    add_task(data_dir, _make_task(title='Todo task', status='Todo'))
    runner = CliRunner()
    result = runner.invoke(
        list_tasks, ['--status', 'Now', '--status', 'Todo', '--json']
    )
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert len(payload) == 2


# --- edit ---


def test_edit_updates_title(data_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    saved = add_task(data_dir, _make_task(title='Old title'))
    runner = CliRunner()
    result = runner.invoke(edit, [saved.id, '--title', 'New title'])
    assert result.exit_code == 0
    assert '✓ Task updated: New title' in result.output


def test_edit_no_fields_is_error(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    saved = add_task(data_dir, _make_task())
    runner = CliRunner()
    result = runner.invoke(edit, [saved.id])
    assert result.exit_code != 0


def test_edit_unknown_id_is_error(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    runner = CliRunner()
    result = runner.invoke(edit, ['xxxxxxxx', '--title', 'X'])
    assert result.exit_code != 0
    assert 'xxxxxxxx' in result.output


def test_edit_invalid_status_is_error(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    saved = add_task(data_dir, _make_task())
    runner = CliRunner()
    result = runner.invoke(edit, [saved.id, '--status', 'NotAStatus'])
    assert result.exit_code != 0
    assert 'Invalid status' in result.output


def test_edit_json_returns_updated_task(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    saved = add_task(data_dir, _make_task(title='Before'))
    runner = CliRunner()
    result = runner.invoke(edit, [saved.id, '--title', 'After', '--json'])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload['title'] == 'After'
    assert payload['id'] == saved.id


# --- delete ---


def test_delete_with_yes_removes_task(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    saved = add_task(data_dir, _make_task(title='Bye'))
    runner = CliRunner()
    result = runner.invoke(delete, [saved.id, '--yes'])
    assert result.exit_code == 0
    assert '✓ Task deleted: Bye' in result.output


def test_delete_confirm_n_aborts(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    saved = add_task(data_dir, _make_task(title='Keep me'))
    runner = CliRunner()
    result = runner.invoke(delete, [saved.id], input='n\n')
    assert result.exit_code == 0
    from knbn.model.store import load_tasks

    assert len(load_tasks(data_dir)) == 1


def test_delete_unknown_id_is_error(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    ensure_data_dir(data_dir)
    runner = CliRunner()
    result = runner.invoke(delete, ['xxxxxxxx', '--yes'])
    assert result.exit_code != 0
    assert 'xxxxxxxx' in result.output


# --- config ---


def test_config_outputs_valid_json(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    result = runner.invoke(config, [])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    for key in [
        'active_statuses',
        'default_active_status',
        'terminal_statuses',
        'default_terminal_status',
        'priorities',
        'categories',
        'free_text_fields',
        'data_dir',
    ]:
        assert key in payload


def test_config_data_dir_is_absolute(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    result = runner.invoke(config, [])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert Path(payload['data_dir']).is_absolute()
