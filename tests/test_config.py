"""Tests for config module."""

from pathlib import Path

import pytest

from knbn.config import (
    CategoryConfig,
    build_default_board_config,
    load_board_config,
    load_default_board_config,
    resolve_data_dir,
    save_board_config,
    save_settings,
)


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


def test_save_board_config_round_trip(tmp_path: Path) -> None:
    config = build_default_board_config()
    original_color = config.categories[0].color
    new_color = '#aabbcc'
    assert original_color != new_color

    updated_categories = [
        CategoryConfig(name=c.name, color=new_color if i == 0 else c.color)
        for i, c in enumerate(config.categories)
    ]
    from dataclasses import replace

    updated_config = replace(config, categories=updated_categories)
    save_board_config(tmp_path, updated_config)

    loaded = load_board_config(tmp_path)
    assert loaded.categories[0].color == new_color
    assert all(
        loaded.categories[i].color == config.categories[i].color
        for i in range(1, len(config.categories))
    )


def test_save_board_config_preserves_app_block(tmp_path: Path) -> None:
    settings = {'app': {'theme': 'nord', 'deadline_warning_hours': '48'}, 'board': {}}
    save_settings(tmp_path, settings)

    config = build_default_board_config()
    save_board_config(tmp_path, config)

    import json

    saved = json.loads((tmp_path / 'settings.json').read_text())
    assert saved['app']['theme'] == 'nord'
    assert saved['app']['deadline_warning_hours'] == '48'


def test_save_board_config_is_atomic(tmp_path: Path) -> None:
    config = build_default_board_config()
    save_board_config(tmp_path, config)

    tmp_file = tmp_path / '.settings.json.tmp'
    assert not tmp_file.exists(), 'tmp file should be renamed, not left behind'
    assert (tmp_path / 'settings.json').exists()
