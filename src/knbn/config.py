"""Data directory resolution, user settings, and board configuration."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any

_ENV_VAR = 'KNBN_DATA_DIR'
_DEFAULT_DIR = Path.home() / '.knbn'
_SETTINGS_FILENAME = 'settings.json'
_SETTINGS_TMP_FILENAME = '.settings.json.tmp'

_HEX_COLOR_RE = re.compile(r'^#[0-9a-f]{6}$')
NAME_MIN = 2
NAME_MAX = 20

CATEGORY_COLOR_PALETTE: list[str] = [
    '#e879a0',
    '#f4a7b9',
    '#7ec8e3',
    '#5b9bd5',
    '#4dbfbf',
    '#f5a623',
    '#cccccc',
    '#a78bfa',
    '#34d399',
    '#fbbf24',
]


class BoardConfigError(Exception):
    """Raised when board configuration in settings.json is invalid."""


@dataclass
class CategoryConfig:
    name: str
    color: str


@dataclass
class BoardConfig:
    active_statuses: list[str]
    default_active_status: str
    terminal_statuses: list[str]
    default_terminal_status: str
    priorities: list[str]
    categories: list[CategoryConfig]
    free_text_fields: list[str]

    def category_color(self, name: str) -> str:
        for cat in self.categories:
            if cat.name == name:
                return cat.color
        return '#888888'

    def active_free_text_fields(self) -> list[tuple[int, str]]:
        return [(i, label) for i, label in enumerate(self.free_text_fields) if label]

    def all_statuses(self) -> list[str]:
        return self.active_statuses + self.terminal_statuses


def load_default_board_config() -> dict[str, Any]:
    """Return the board config block from the bundled defaults/settings.json."""
    resource = files('knbn').joinpath('defaults/settings.json')
    try:
        raw = resource.read_text(encoding='utf-8')
    except (FileNotFoundError, OSError) as exc:
        raise RuntimeError(
            f'knbn defaults file not found — package may be incomplete: {exc}'
        ) from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f'knbn defaults/settings.json is not valid JSON: {exc}'
        ) from exc
    return dict(data['board'])


SETTINGS_DEFAULTS: dict[str, Any] = {
    'app': {
        'theme': 'textual-dark',
        'deadline_warning_hours': '24',
    },
}


def resolve_data_dir() -> Path:
    env_val = os.environ.get(_ENV_VAR)
    if env_val:
        return Path(env_val)
    return _DEFAULT_DIR


def load_settings(data_dir: Path) -> dict[str, Any]:
    settings_file = data_dir / _SETTINGS_FILENAME
    result: dict[str, Any] = {
        'app': dict(SETTINGS_DEFAULTS['app']),
    }
    if not settings_file.exists():
        return result
    try:
        raw = json.loads(settings_file.read_text(encoding='utf-8'))
        if isinstance(raw, dict):
            if 'app' in raw and isinstance(raw['app'], dict):
                result['app'].update(raw['app'])
            if 'board' in raw:
                result['board'] = raw['board']
    except (json.JSONDecodeError, OSError):
        pass
    return result


def save_settings(data_dir: Path, settings: dict[str, Any]) -> None:
    tmp_file = data_dir / _SETTINGS_TMP_FILENAME
    tmp_file.write_text(json.dumps(settings, indent=2), encoding='utf-8')
    tmp_file.rename(data_dir / _SETTINGS_FILENAME)


def get_app_setting(data_dir: Path, key: str, default: Any = '') -> Any:
    settings = load_settings(data_dir)
    return settings.get('app', {}).get(key, default)


def _validate_name(value: str, field: str) -> None:
    if not (NAME_MIN <= len(value) <= NAME_MAX):
        raise BoardConfigError(
            f'{field} name {value!r} must be between {NAME_MIN} and {NAME_MAX} characters'
        )


def build_default_board_config() -> BoardConfig:
    d = load_default_board_config()
    categories = [
        CategoryConfig(name=c['name'], color=c['color']) for c in d['categories']
    ]
    return BoardConfig(
        active_statuses=list(d['active_statuses']),
        default_active_status=d['default_active_status'],
        terminal_statuses=list(d['terminal_statuses']),
        default_terminal_status=d['default_terminal_status'],
        priorities=list(d['priorities']),
        categories=categories,
        free_text_fields=_parse_free_text_fields(d),
    )


def _parse_active_statuses(board: dict[str, Any]) -> tuple[list[str], str]:
    active = board.get('active_statuses', [])
    if not isinstance(active, list) or not (2 <= len(active) <= 5):
        raise BoardConfigError(
            f'active_statuses must have 2-5 entries, got '
            f'{len(active) if isinstance(active, list) else "invalid"}'
        )
    for name in active:
        _validate_name(str(name), 'active_statuses')
    default = board.get('default_active_status', '')
    if default not in active:
        raise BoardConfigError(
            f'default_active_status {default!r} not found in active_statuses'
        )
    return [str(s) for s in active], str(default)


def _parse_terminal_statuses(board: dict[str, Any]) -> tuple[list[str], str]:
    terminal = board.get('terminal_statuses', [])
    if not isinstance(terminal, list) or not (1 <= len(terminal) <= 3):
        raise BoardConfigError(
            f'terminal_statuses must have 1-3 entries, got '
            f'{len(terminal) if isinstance(terminal, list) else "invalid"}'
        )
    for name in terminal:
        _validate_name(str(name), 'terminal_statuses')
    default = board.get('default_terminal_status', '')
    if default not in terminal:
        raise BoardConfigError(
            f'default_terminal_status {default!r} not found in terminal_statuses'
        )
    return [str(s) for s in terminal], str(default)


def _parse_priorities(board: dict[str, Any]) -> list[str]:
    priorities = board.get('priorities', [])
    if not isinstance(priorities, list) or not (1 <= len(priorities) <= 5):
        raise BoardConfigError(
            f'priorities must have 1-5 entries, got '
            f'{len(priorities) if isinstance(priorities, list) else "invalid"}'
        )
    for name in priorities:
        _validate_name(str(name), 'priorities')
    return [str(p) for p in priorities]


def _parse_categories(board: dict[str, Any]) -> list[CategoryConfig]:
    raw_cats = board.get('categories', [])
    if not isinstance(raw_cats, list) or not (1 <= len(raw_cats) <= 10):
        raise BoardConfigError(
            f'categories must have 1-10 entries, got '
            f'{len(raw_cats) if isinstance(raw_cats, list) else "invalid"}'
        )
    categories: list[CategoryConfig] = []
    for cat in raw_cats:
        if not isinstance(cat, dict):
            raise BoardConfigError(
                'each category must be a JSON object with name and color'
            )
        cat_name = str(cat.get('name', ''))
        cat_color = str(cat.get('color', ''))
        _validate_name(cat_name, 'categories')
        if not _HEX_COLOR_RE.match(cat_color):
            raise BoardConfigError(
                f'category color {cat_color!r} must match #[0-9a-f]{{6}}'
            )
        categories.append(CategoryConfig(name=cat_name, color=cat_color))
    return categories


def _parse_free_text_fields(board: dict[str, Any]) -> list[str]:
    raw = board.get('free_text_fields', [])
    if not isinstance(raw, list) or len(raw) > 3:
        raise BoardConfigError(
            f'free_text_fields must have 0-3 entries, got '
            f'{len(raw) if isinstance(raw, list) else "invalid"}'
        )
    fields: list[str] = []
    for label in raw:
        label_str = str(label)
        if label_str and not (NAME_MIN <= len(label_str) <= NAME_MAX):
            raise BoardConfigError(
                f'free_text_fields label {label_str!r} must be between '
                f'{NAME_MIN} and {NAME_MAX} characters'
            )
        fields.append(label_str)
    while len(fields) < 3:
        fields.append('')
    return fields


def load_board_config(data_dir: Path) -> BoardConfig:
    settings_file = data_dir / _SETTINGS_FILENAME
    if not settings_file.exists():
        return build_default_board_config()
    try:
        raw = json.loads(settings_file.read_text(encoding='utf-8'))
        if not isinstance(raw, dict) or 'board' not in raw:
            return build_default_board_config()
        board = raw['board']
    except (json.JSONDecodeError, OSError):
        return build_default_board_config()
    if not isinstance(board, dict):
        raise BoardConfigError('board block must be a JSON object')
    active, default_active = _parse_active_statuses(board)
    terminal, default_terminal = _parse_terminal_statuses(board)
    priorities = _parse_priorities(board)
    categories = _parse_categories(board)
    free_text_fields = _parse_free_text_fields(board)
    return BoardConfig(
        active_statuses=active,
        default_active_status=default_active,
        terminal_statuses=terminal,
        default_terminal_status=default_terminal,
        priorities=priorities,
        categories=categories,
        free_text_fields=free_text_fields,
    )
