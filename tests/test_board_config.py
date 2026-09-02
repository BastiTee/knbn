"""Tests for BoardConfig loading and validation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from knbn.config import (
    BoardConfig,
    BoardConfigError,
    CategoryConfig,
    build_default_board_config,
    load_board_config,
)


def _write_board(tmp_path: Path, board: dict) -> None:
    (tmp_path / 'settings.json').write_text(
        json.dumps({'app': {}, 'board': board}), encoding='utf-8'
    )


def _valid_board() -> dict:
    return {
        'active_statuses': ['Todo', 'Now', 'Feedback'],
        'default_active_status': 'Now',
        'terminal_statuses': ['Done', 'Stopped'],
        'default_terminal_status': 'Done',
        'priorities': ['High', 'Medium', 'Low'],
        'categories': [{'name': 'Work', 'color': '#e879a0'}],
        'free_text_fields': ['Notes', '', ''],
    }


# --- defaults ---


def test_missing_file_returns_defaults(tmp_path: Path) -> None:
    cfg = load_board_config(tmp_path)
    assert cfg.active_statuses == ['Todo', 'Now', 'Feedback']
    assert cfg.default_terminal_status == 'Done'
    assert cfg.priorities == ['High', 'Medium', 'Low']


def test_missing_board_key_returns_defaults(tmp_path: Path) -> None:
    (tmp_path / 'settings.json').write_text('{"app": {}}', encoding='utf-8')
    cfg = load_board_config(tmp_path)
    assert cfg.active_statuses == ['Todo', 'Now', 'Feedback']


def test_malformed_json_returns_defaults(tmp_path: Path) -> None:
    (tmp_path / 'settings.json').write_text('not json', encoding='utf-8')
    cfg = load_board_config(tmp_path)
    assert cfg.priorities == ['High', 'Medium', 'Low']


# --- valid config ---


def test_valid_config_loads(tmp_path: Path) -> None:
    _write_board(tmp_path, _valid_board())
    cfg = load_board_config(tmp_path)
    assert cfg.active_statuses == ['Todo', 'Now', 'Feedback']
    assert cfg.default_active_status == 'Now'
    assert cfg.terminal_statuses == ['Done', 'Stopped']
    assert cfg.default_terminal_status == 'Done'
    assert cfg.priorities == ['High', 'Medium', 'Low']
    assert cfg.categories[0].name == 'Work'
    assert cfg.free_text_fields == ['Notes', '', '']


# --- active_statuses validation ---


def test_too_few_active_statuses_raises(tmp_path: Path) -> None:
    b = _valid_board()
    b['active_statuses'] = ['Only']
    b['default_active_status'] = 'Only'
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError, match='active_statuses'):
        load_board_config(tmp_path)


def test_too_many_active_statuses_raises(tmp_path: Path) -> None:
    b = _valid_board()
    b['active_statuses'] = ['A', 'B', 'C', 'D', 'E', 'F']
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError, match='active_statuses'):
        load_board_config(tmp_path)


def test_status_name_too_short_raises(tmp_path: Path) -> None:
    b = _valid_board()
    b['active_statuses'] = ['X', 'Now']
    b['default_active_status'] = 'X'
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError, match="'X'"):
        load_board_config(tmp_path)


def test_status_name_too_long_raises(tmp_path: Path) -> None:
    long_name = 'A' * 21
    b = _valid_board()
    b['active_statuses'] = [long_name, 'Now']
    b['default_active_status'] = long_name
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError):
        load_board_config(tmp_path)


def test_default_active_status_not_in_list_raises(tmp_path: Path) -> None:
    b = _valid_board()
    b['default_active_status'] = 'NotInList'
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError, match='default_active_status'):
        load_board_config(tmp_path)


# --- terminal_statuses validation ---


def test_default_terminal_status_not_in_list_raises(tmp_path: Path) -> None:
    b = _valid_board()
    b['default_terminal_status'] = 'NotInList'
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError, match='default_terminal_status'):
        load_board_config(tmp_path)


# --- priorities validation ---


def test_priority_name_min_length_accepted(tmp_path: Path) -> None:
    b = _valid_board()
    b['priorities'] = ['Hi', 'Lo']
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert cfg.priorities == ['Hi', 'Lo']


def test_too_many_priorities_raises(tmp_path: Path) -> None:
    b = _valid_board()
    b['priorities'] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError, match='priorities'):
        load_board_config(tmp_path)


# --- categories validation ---


def test_category_name_max_length_accepted(tmp_path: Path) -> None:
    b = _valid_board()
    b['categories'] = [{'name': 'A' * 20, 'color': '#aabbcc'}]
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert len(cfg.categories[0].name) == 20


def test_category_name_too_long_raises(tmp_path: Path) -> None:
    b = _valid_board()
    b['categories'] = [{'name': 'A' * 21, 'color': '#aabbcc'}]
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError):
        load_board_config(tmp_path)


def test_too_many_categories_raises(tmp_path: Path) -> None:
    b = _valid_board()
    b['categories'] = [{'name': f'Cat{i:02d}', 'color': '#aabbcc'} for i in range(11)]
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError, match='categories'):
        load_board_config(tmp_path)


# --- category color validation ---


def test_valid_hex_color_accepted(tmp_path: Path) -> None:
    b = _valid_board()
    b['categories'] = [{'name': 'Work', 'color': '#4dbfbf'}]
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert cfg.categories[0].color == '#4dbfbf'


def test_short_hex_rejected(tmp_path: Path) -> None:
    b = _valid_board()
    b['categories'] = [{'name': 'Work', 'color': '#fff'}]
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError, match='color'):
        load_board_config(tmp_path)


def test_uppercase_hex_rejected(tmp_path: Path) -> None:
    b = _valid_board()
    b['categories'] = [{'name': 'Work', 'color': '#4DBFBF'}]
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError, match='color'):
        load_board_config(tmp_path)


def test_missing_hash_rejected(tmp_path: Path) -> None:
    b = _valid_board()
    b['categories'] = [{'name': 'Work', 'color': '4dbfbf'}]
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError, match='color'):
        load_board_config(tmp_path)


# --- free_text_fields validation ---


def test_free_text_label_too_short_raises(tmp_path: Path) -> None:
    b = _valid_board()
    b['free_text_fields'] = ['X']
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError, match="'X'"):
        load_board_config(tmp_path)


def test_free_text_label_max_length_accepted(tmp_path: Path) -> None:
    b = _valid_board()
    b['free_text_fields'] = ['A' * 20]
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert cfg.free_text_fields[0] == 'A' * 20


def test_free_text_label_too_long_raises(tmp_path: Path) -> None:
    b = _valid_board()
    b['free_text_fields'] = ['A' * 21]
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError):
        load_board_config(tmp_path)


def test_empty_free_text_label_accepted(tmp_path: Path) -> None:
    b = _valid_board()
    b['free_text_fields'] = ['', '', '']
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert cfg.free_text_fields == ['', '', '']


def test_too_many_free_text_fields_raises(tmp_path: Path) -> None:
    b = _valid_board()
    b['free_text_fields'] = ['AA', 'BB', 'CC', 'DD']
    _write_board(tmp_path, b)
    with pytest.raises(BoardConfigError, match='free_text_fields'):
        load_board_config(tmp_path)


def test_free_text_fields_padded_to_three(tmp_path: Path) -> None:
    b = _valid_board()
    b['free_text_fields'] = ['Notes']
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert len(cfg.free_text_fields) == 3
    assert cfg.free_text_fields == ['Notes', '', '']


# --- BoardConfig helpers ---


def test_category_color_returns_configured(tmp_path: Path) -> None:
    _write_board(tmp_path, _valid_board())
    cfg = load_board_config(tmp_path)
    assert cfg.category_color('Work') == '#e879a0'


def test_category_color_fallback_for_unknown(tmp_path: Path) -> None:
    _write_board(tmp_path, _valid_board())
    cfg = load_board_config(tmp_path)
    assert cfg.category_color('UnknownTag') == '#888888'


def test_active_free_text_fields_skips_empty(tmp_path: Path) -> None:
    b = _valid_board()
    b['free_text_fields'] = ['Feedback From', '', 'Notes']
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert cfg.active_free_text_fields() == [(0, 'Feedback From'), (2, 'Notes')]


def test_active_free_text_fields_all_empty(tmp_path: Path) -> None:
    b = _valid_board()
    b['free_text_fields'] = ['', '', '']
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert cfg.active_free_text_fields() == []


def test_all_statuses_concatenates(tmp_path: Path) -> None:
    _write_board(tmp_path, _valid_board())
    cfg = load_board_config(tmp_path)
    assert cfg.all_statuses() == ['Todo', 'Now', 'Feedback', 'Done', 'Stopped']


# --- build_default_board_config ---


def test_build_default_board_config_returns_legacy_defaults() -> None:
    cfg = build_default_board_config()
    assert isinstance(cfg, BoardConfig)
    assert cfg.active_statuses == ['Todo', 'Now', 'Feedback']
    assert cfg.default_active_status == 'Todo'
    assert cfg.terminal_statuses == ['Done', 'Delegated', 'Stopped']
    assert cfg.default_terminal_status == 'Done'
    assert cfg.priorities == ['High', 'Medium', 'Low']
    assert len(cfg.categories) == 5
    assert isinstance(cfg.categories[0], CategoryConfig)
    assert cfg.free_text_fields == ['Feedback From', 'Delegated To', '']


# --- multi-word names ---


def test_multi_word_status_names_accepted(tmp_path: Path) -> None:
    b = _valid_board()
    b['active_statuses'] = ['In Progress', 'Not Started', 'On Hold']
    b['default_active_status'] = 'In Progress'
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert cfg.active_statuses == ['In Progress', 'Not Started', 'On Hold']
    assert cfg.default_active_status == 'In Progress'


def test_multi_word_terminal_status_accepted(tmp_path: Path) -> None:
    b = _valid_board()
    b['terminal_statuses'] = ['Not Done', 'Handed Off']
    b['default_terminal_status'] = 'Not Done'
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert cfg.terminal_statuses == ['Not Done', 'Handed Off']


def test_multi_word_priority_names_accepted(tmp_path: Path) -> None:
    b = _valid_board()
    b['priorities'] = ['Very High', 'Medium', 'Very Low']
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert cfg.priorities == ['Very High', 'Medium', 'Very Low']


def test_multi_word_category_name_accepted(tmp_path: Path) -> None:
    b = _valid_board()
    b['categories'] = [{'name': 'Senior Task', 'color': '#e879a0'}]
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert cfg.categories[0].name == 'Senior Task'


def test_multi_word_free_text_label_accepted(tmp_path: Path) -> None:
    b = _valid_board()
    b['free_text_fields'] = ['Blocked By', 'Review From']
    _write_board(tmp_path, b)
    cfg = load_board_config(tmp_path)
    assert cfg.free_text_fields[:2] == ['Blocked By', 'Review From']
