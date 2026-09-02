"""Tests for config module."""

from pathlib import Path

import pytest

from knbn.config import load_default_board_config, resolve_data_dir


def test_load_default_board_config_returns_board_keys() -> None:
    board = load_default_board_config()
    assert 'active_statuses' in board
    assert 'terminal_statuses' in board
    assert 'priorities' in board
    assert 'categories' in board
    assert 'free_text_fields' in board


def test_load_default_board_config_is_not_empty() -> None:
    board = load_default_board_config()
    assert len(board['active_statuses']) >= 2
    assert len(board['priorities']) >= 1
    assert len(board['categories']) >= 1


def test_default_data_dir(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv('KNBN_DATA_DIR', raising=False)
    assert resolve_data_dir() == Path.home() / '.knbn'


def test_env_var_override(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(tmp_path))
    assert resolve_data_dir() == tmp_path
