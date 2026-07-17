"""Tests for CLI commands."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from knbn.cli import add, init
from knbn.model.task import Task


@pytest.fixture()
def data_dir(tmp_path: Path) -> Path:
    return tmp_path / 'knbn'


def test_init_creates_data_dir(data_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    result = runner.invoke(init)
    assert result.exit_code == 0
    assert data_dir.is_dir()
    assert (data_dir / 'tasks.csv').exists()
    assert (data_dir / 'notes').is_dir()
    assert 'Initialized' in result.output


def test_init_idempotent(data_dir: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    runner.invoke(init)
    result = runner.invoke(init)
    assert result.exit_code == 0
    assert 'Already initialized' in result.output


def test_init_with_explicit_path(tmp_path: Path) -> None:
    target = tmp_path / 'custom'
    runner = CliRunner()
    result = runner.invoke(init, [str(target)])
    assert result.exit_code == 0
    assert target.is_dir()


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
    assert task.category == 'Ideas'
    assert task.key_resource == ''


def test_add_fast_flag_sets_all_defaults(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(add, ['-f', '--title', 'Quick task'])
    assert result.exit_code == 0
    task: Task = mock_add.call_args[0][1]
    assert task.status == 'Todo'
    assert task.priority == 'Medium'
    assert task.category == 'Ideas'


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


def test_add_confirmation_message(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    with patch('knbn.cli.add_task'):
        result = runner.invoke(add, ['--fast', '--title', 'Confirm me'])
    assert '✓ Task added: Confirm me' in result.output


def test_add_interactive_prompts_full(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test add with all prompts answered interactively (no flags)."""
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    # Inputs: title, status (1=Todo), priority (1=High), category (1=People), resource (empty)
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(add, [], input='Interactive task\n1\n1\n1\n\n')
    assert result.exit_code == 0
    assert '✓ Task added: Interactive task' in result.output
    task: Task = mock_add.call_args[0][1]
    assert task.title == 'Interactive task'
    assert task.status == 'Todo'
    assert task.priority == 'High'
    assert task.category == 'People'
    assert task.key_resource == ''


def test_add_interactive_feedback_status(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Selecting Feedback status prompts for Feedback From."""
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    # status list: 1=Todo,2=Now,3=Feedback — pick 3; then feedback_from; priority default; category default; no resource
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(
            add,
            [
                '--title',
                'Blocked task',
                '--priority-default',
                '--category-default',
                '--no-resource',
            ],
            input='3\nCarol\n',
        )
    assert result.exit_code == 0
    task: Task = mock_add.call_args[0][1]
    assert task.status == 'Feedback'
    assert task.feedback_from == 'Carol'


def test_add_interactive_delegated_status(
    data_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Selecting Delegated status prompts for Delegated To."""
    monkeypatch.setenv('KNBN_DATA_DIR', str(data_dir))
    runner = CliRunner()
    # status: 4=Delegated
    with patch('knbn.cli.add_task') as mock_add:
        result = runner.invoke(
            add,
            [
                '--title',
                'Hand off',
                '--priority-default',
                '--category-default',
                '--no-resource',
            ],
            input='4\nAlex\n',
        )
    assert result.exit_code == 0
    task: Task = mock_add.call_args[0][1]
    assert task.status == 'Delegated'
    assert task.delegated_to == 'Alex'


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
            ],
            input='-\n',
        )
    assert result.exit_code == 0
    task: Task = mock_add.call_args[0][1]
    assert task.key_resource == ''
