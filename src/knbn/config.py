"""Data directory resolution and user settings."""

from __future__ import annotations

import json
import os
from pathlib import Path

_ENV_VAR = 'KNBN_DATA_DIR'
_DEFAULT_DIR = Path.home() / '.knbn'
_SETTINGS_FILENAME = 'settings.json'
_SETTINGS_TMP_FILENAME = '.settings.json.tmp'

SETTINGS_DEFAULTS: dict[str, str] = {
    'theme': 'textual-dark',
}


def resolve_data_dir() -> Path:
    env_val = os.environ.get(_ENV_VAR)
    if env_val:
        return Path(env_val)
    return _DEFAULT_DIR


def load_settings(data_dir: Path) -> dict[str, str]:
    settings_file = data_dir / _SETTINGS_FILENAME
    result = dict(SETTINGS_DEFAULTS)
    if not settings_file.exists():
        return result
    try:
        raw = json.loads(settings_file.read_text(encoding='utf-8'))
        if isinstance(raw, dict):
            result.update({str(k): str(v) for k, v in raw.items()})
    except (json.JSONDecodeError, OSError):
        pass
    return result


def save_settings(data_dir: Path, settings: dict[str, str]) -> None:
    tmp_file = data_dir / _SETTINGS_TMP_FILENAME
    tmp_file.write_text(json.dumps(settings, indent=2), encoding='utf-8')
    tmp_file.rename(data_dir / _SETTINGS_FILENAME)


def get_setting(data_dir: Path, key: str, default: str = '') -> str:
    settings = load_settings(data_dir)
    return settings.get(key, default)
