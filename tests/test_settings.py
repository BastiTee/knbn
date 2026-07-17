"""Tests for settings load/save helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from knbn.config import SETTINGS_DEFAULTS, get_setting, load_settings, save_settings


def test_load_returns_defaults_for_missing_file(tmp_path: Path) -> None:
    result = load_settings(tmp_path)
    assert result == SETTINGS_DEFAULTS
    assert result['theme'] == 'textual-dark'


def test_load_returns_defaults_for_missing_settings_key(tmp_path: Path) -> None:
    save_settings(tmp_path, {})
    result = load_settings(tmp_path)
    assert result['theme'] == 'textual-dark'


def test_round_trip(tmp_path: Path) -> None:
    settings = {'theme': 'textual-light'}
    save_settings(tmp_path, settings)
    loaded = load_settings(tmp_path)
    assert loaded['theme'] == 'textual-light'


def test_load_merges_missing_keys_with_defaults(tmp_path: Path) -> None:
    save_settings(tmp_path, {'theme': 'light'})
    loaded = load_settings(tmp_path)
    for key in SETTINGS_DEFAULTS:
        assert key in loaded


def test_load_tolerates_malformed_json(tmp_path: Path) -> None:
    (tmp_path / 'settings.json').write_text('not json', encoding='utf-8')
    result = load_settings(tmp_path)
    assert result == SETTINGS_DEFAULTS


def test_atomic_save_uses_tmp_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    renamed_from: list[Path] = []
    original_rename = Path.rename

    def capturing_rename(self: Path, target: Path) -> Path:
        renamed_from.append(self)
        return original_rename(self, target)

    monkeypatch.setattr(Path, 'rename', capturing_rename)
    save_settings(tmp_path, {'theme': 'dark'})
    assert any('.settings.json.tmp' in str(p) for p in renamed_from)


def test_get_setting_present_key(tmp_path: Path) -> None:
    save_settings(tmp_path, {'theme': 'textual-light'})
    assert get_setting(tmp_path, 'theme') == 'textual-light'


def test_get_setting_absent_key_returns_default(tmp_path: Path) -> None:
    assert get_setting(tmp_path, 'nonexistent', 'fallback') == 'fallback'


def test_get_setting_absent_key_empty_default(tmp_path: Path) -> None:
    assert get_setting(tmp_path, 'nonexistent') == ''
