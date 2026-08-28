"""Tests for settings load/save helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from knbn.config import (
    SETTINGS_DEFAULTS,
    get_app_setting,
    load_settings,
    save_settings,
)


def test_load_returns_defaults_for_missing_file(tmp_path: Path) -> None:
    result = load_settings(tmp_path)
    assert result['app']['theme'] == 'textual-dark'
    assert result['app']['deadline_warning_hours'] == '24'


def test_load_returns_defaults_for_missing_app_key(tmp_path: Path) -> None:
    save_settings(tmp_path, {})
    result = load_settings(tmp_path)
    assert result['app']['theme'] == 'textual-dark'


def test_round_trip(tmp_path: Path) -> None:
    settings: dict = {'app': {'theme': 'textual-light'}, 'board': {}}
    save_settings(tmp_path, settings)
    loaded = load_settings(tmp_path)
    assert loaded['app']['theme'] == 'textual-light'


def test_load_merges_app_defaults_for_missing_keys(tmp_path: Path) -> None:
    save_settings(tmp_path, {'app': {'theme': 'light'}})
    loaded = load_settings(tmp_path)
    for key in SETTINGS_DEFAULTS['app']:
        assert key in loaded['app']


def test_load_tolerates_malformed_json(tmp_path: Path) -> None:
    (tmp_path / 'settings.json').write_text('not json', encoding='utf-8')
    result = load_settings(tmp_path)
    assert result['app']['theme'] == 'textual-dark'


def test_atomic_save_uses_tmp_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    renamed_from: list[Path] = []
    original_rename = Path.rename

    def capturing_rename(self: Path, target: Path) -> Path:
        renamed_from.append(self)
        return original_rename(self, target)

    monkeypatch.setattr(Path, 'rename', capturing_rename)
    save_settings(tmp_path, {'app': {'theme': 'dark'}, 'board': {}})
    assert any('.settings.json.tmp' in str(p) for p in renamed_from)


def test_both_blocks_preserved_on_save(tmp_path: Path) -> None:
    settings: dict = {'app': {'theme': 'nord'}, 'board': {'active_statuses': ['Todo']}}
    save_settings(tmp_path, settings)
    loaded = load_settings(tmp_path)
    assert loaded['app']['theme'] == 'nord'
    assert loaded['board']['active_statuses'] == ['Todo']


def test_get_app_setting_present_key(tmp_path: Path) -> None:
    save_settings(tmp_path, {'app': {'theme': 'textual-light'}, 'board': {}})
    assert get_app_setting(tmp_path, 'theme') == 'textual-light'


def test_get_app_setting_absent_key_returns_default(tmp_path: Path) -> None:
    assert get_app_setting(tmp_path, 'nonexistent', 'fallback') == 'fallback'


def test_get_app_setting_absent_key_empty_default(tmp_path: Path) -> None:
    assert get_app_setting(tmp_path, 'nonexistent') == ''


def test_get_app_setting_deadline_warning_hours(tmp_path: Path) -> None:
    save_settings(tmp_path, {'app': {'deadline_warning_hours': '48'}, 'board': {}})
    raw = get_app_setting(tmp_path, 'deadline_warning_hours', '24')
    assert int(raw) == 48


def test_get_app_setting_missing_returns_default_int(tmp_path: Path) -> None:
    raw = get_app_setting(tmp_path, 'deadline_warning_hours', '24')
    assert int(raw) == 24
