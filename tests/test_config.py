"""Tests for config module."""

from pathlib import Path

import pytest

from knbn.config import resolve_data_dir


def test_default_data_dir(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv('KNBN_DATA_DIR', raising=False)
    assert resolve_data_dir() == Path.home() / '.knbn'


def test_env_var_override(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(tmp_path))
    assert resolve_data_dir() == tmp_path


def test_env_var_is_path_object(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv('KNBN_DATA_DIR', str(tmp_path))
    result = resolve_data_dir()
    assert isinstance(result, Path)
