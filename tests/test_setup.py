"""Tests for the board setup wizard."""

from __future__ import annotations

from pathlib import Path

import click
import pytest
from click.testing import CliRunner

from knbn.config import (
    CATEGORY_COLOR_PALETTE,
    load_board_config,
    load_default_board_config,
)
from knbn.setup import run_setup_wizard, should_run_wizard


@click.command()
@click.argument('path')
def _invoke_wizard(path: str) -> None:
    run_setup_wizard(Path(path))


# --- should_run_wizard ---


def test_should_run_wizard_fresh_dir(tmp_path: Path) -> None:
    assert should_run_wizard(tmp_path) is True


def test_should_run_wizard_csv_exists(tmp_path: Path) -> None:
    (tmp_path / 'tasks.csv').touch()
    assert should_run_wizard(tmp_path) is False


def test_should_run_wizard_board_key_exists(tmp_path: Path) -> None:
    (tmp_path / 'settings.json').write_text('{"board": {}}', encoding='utf-8')
    assert should_run_wizard(tmp_path) is False


def test_should_run_wizard_settings_without_board_key(tmp_path: Path) -> None:
    (tmp_path / 'settings.json').write_text('{"app": {}}', encoding='utf-8')
    assert should_run_wizard(tmp_path) is True


def test_should_run_wizard_malformed_settings(tmp_path: Path) -> None:
    (tmp_path / 'settings.json').write_text('not json', encoding='utf-8')
    assert should_run_wizard(tmp_path) is True


# --- run_setup_wizard ---
# Active(2): Todo Now | Terminal(1): Done | Priorities(2): High Low | Cat(1): Work | FTF: all blank
_MINIMAL_INPUT = 'n\nTodo\nNow\n\nDone\n\nHigh\nLow\n\nWork\n\n\n\n\n'


def test_wizard_minimal_creates_config(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input=_MINIMAL_INPUT)
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    assert cfg.active_statuses == ['Todo', 'Now']
    assert cfg.default_active_status == 'Todo'
    assert cfg.terminal_statuses == ['Done']
    assert cfg.default_terminal_status == 'Done'
    assert cfg.priorities == ['High', 'Low']
    assert cfg.categories[0].name == 'Work'
    assert cfg.free_text_fields == ['', '', '']


def test_wizard_settings_file_has_board_key(tmp_path: Path) -> None:
    runner = CliRunner()
    runner.invoke(_invoke_wizard, [str(tmp_path)], input=_MINIMAL_INPUT)
    assert not should_run_wizard(tmp_path)


def test_wizard_with_free_text_label(tmp_path: Path) -> None:
    # Active(2), Terminal(1), Priority(1), Cat(1), FTF1=Notes blank blank
    wizard_input = 'n\nTodo\nNow\n\nDone\n\nHigh\n\nWork\n\nNotes\n\n\n'
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input=wizard_input)
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    assert cfg.free_text_fields[0] == 'Notes'
    assert cfg.free_text_fields[1] == ''
    assert cfg.free_text_fields[2] == ''


def test_wizard_multiple_terminal_statuses_with_default(tmp_path: Path) -> None:
    # Active(2), Terminal(2): Done Archived → select 2 as default | Prio(1) Cat(1) FTF blank
    wizard_input = 'n\nTodo\nNow\n\nDone\nArchived\n\n2\nHi\n\nStuff\n\n\n\n\n'
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input=wizard_input)
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    assert cfg.terminal_statuses == ['Done', 'Archived']
    assert cfg.default_terminal_status == 'Archived'


def test_wizard_auto_assigns_palette_colors(tmp_path: Path) -> None:
    # Two categories → first two palette colors
    wizard_input = 'n\nTodo\nNow\n\nDone\n\nHigh\n\nAlpha\nBeta\n\n\n\n\n'
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input=wizard_input)
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    assert len(cfg.categories) == 2
    assert cfg.categories[0].color == CATEGORY_COLOR_PALETTE[0]
    assert cfg.categories[1].color == CATEGORY_COLOR_PALETTE[1]


def test_wizard_rejects_short_status_name(tmp_path: Path) -> None:
    # 'X' is too short (1 char), then valid names
    wizard_input = 'n\nX\nTodo\nNow\n\nDone\n\nHi\n\nWork\n\n\n\n\n'
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input=wizard_input)
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    assert 'X' not in cfg.active_statuses
    assert cfg.active_statuses == ['Todo', 'Now']


def test_wizard_rejects_long_status_name(tmp_path: Path) -> None:
    long_name = 'A' * 21
    wizard_input = f'n\n{long_name}\nTodo\nNow\n\nDone\n\nHi\n\nWork\n\n\n\n\n'
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input=wizard_input)
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    assert long_name not in cfg.active_statuses
    assert cfg.active_statuses == ['Todo', 'Now']


def test_wizard_rejects_too_few_statuses(tmp_path: Path) -> None:
    # Enter only 1 status then blank → error → try again with 2
    wizard_input = 'n\nOnlyOne\n\nTodo\nNow\n\nDone\n\nHi\n\nWork\n\n\n\n\n'
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input=wizard_input)
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    assert cfg.active_statuses == ['Todo', 'Now']


def test_wizard_rejects_short_free_text_label(tmp_path: Path) -> None:
    # 'X' too short for FTF slot 1, then 'Notes' valid
    wizard_input = 'n\nTodo\nNow\n\nDone\n\nHi\n\nWork\n\nX\nNotes\n\n\n'
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input=wizard_input)
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    assert cfg.free_text_fields[0] == 'Notes'


def test_wizard_rejects_long_free_text_label(tmp_path: Path) -> None:
    long_label = 'B' * 21
    wizard_input = f'n\nTodo\nNow\n\nDone\n\nHi\n\nWork\n\n{long_label}\nNotes\n\n\n'
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input=wizard_input)
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    assert cfg.free_text_fields[0] == 'Notes'


def test_wizard_preserves_existing_app_settings(tmp_path: Path) -> None:
    (tmp_path / 'settings.json').write_text(
        '{"app": {"theme": "nord"}, "board": {}}', encoding='utf-8'
    )
    runner = CliRunner()
    runner.invoke(_invoke_wizard, [str(tmp_path)], input=_MINIMAL_INPUT)
    cfg_raw = load_board_config(tmp_path)
    from knbn.config import get_app_setting

    assert get_app_setting(tmp_path, 'theme') == 'nord'
    assert cfg_raw.active_statuses == ['Todo', 'Now']


@pytest.mark.parametrize('idx', [0, 1, 2])
def test_wizard_free_text_blank_slots(tmp_path: Path, idx: int) -> None:
    # All FTF blank → all empty
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input=_MINIMAL_INPUT)
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    assert cfg.free_text_fields[idx] == ''


def test_wizard_accepts_multi_word_names(tmp_path: Path) -> None:
    # Multi-word status, priority, category, and free-text label
    wizard_input = (
        'n\n'  # decline quick-start
        'In Progress\nNot Started\n\n'  # active statuses
        'Not Done\n\n'  # terminal status
        'Very High\nMedium\n\n'  # priorities
        'Senior Task\n\n'  # category
        'Blocked By\n\n\n'  # FTF: "Blocked By", blank, blank
    )
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input=wizard_input)
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    assert cfg.active_statuses == ['In Progress', 'Not Started']
    assert cfg.terminal_statuses == ['Not Done']
    assert cfg.priorities == ['Very High', 'Medium']
    assert cfg.categories[0].name == 'Senior Task'
    assert cfg.free_text_fields[0] == 'Blocked By'


def test_wizard_quickstart_accept_writes_default_config(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input='\n')
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    defaults = load_default_board_config()
    assert cfg.active_statuses == defaults['active_statuses']
    assert cfg.terminal_statuses == defaults['terminal_statuses']
    assert cfg.priorities == defaults['priorities']
    assert [c.name for c in cfg.categories] == [
        c['name'] for c in defaults['categories']
    ]


def test_wizard_quickstart_decline_proceeds_to_interactive(tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(_invoke_wizard, [str(tmp_path)], input=_MINIMAL_INPUT)
    assert result.exit_code == 0
    cfg = load_board_config(tmp_path)
    assert cfg.active_statuses == ['Todo', 'Now']
