"""First-run board setup wizard."""

from __future__ import annotations

import json
from pathlib import Path

import click

from knbn.config import (
    CATEGORY_COLOR_PALETTE,
    NAME_MAX,
    NAME_MIN,
    SETTINGS_DEFAULTS,
    save_settings,
)


def _collect_names(prompt: str, min_count: int, max_count: int) -> list[str]:
    while True:
        click.echo(
            f'\n{prompt} (one per line, blank line to finish, {min_count}–{max_count}):'
        )
        names: list[str] = []
        while True:
            name = click.prompt('  > ', default='', show_default=False).strip()
            if not name:
                break
            if not (NAME_MIN <= len(name) <= NAME_MAX):
                click.echo(f'  Error: name must be {NAME_MIN}–{NAME_MAX} characters.')
                continue
            names.append(name)
            if len(names) >= max_count:
                break
        if min_count <= len(names) <= max_count:
            return names
        click.echo(
            f'  Error: need {min_count}–{max_count} entries, got {len(names)}. Try again.'
        )


def _collect_free_text_fields() -> list[str]:
    fields: list[str] = []
    click.echo('\nFree-text field labels (0–3, blank to leave slot unused):')
    for i in range(3):
        while True:
            label = click.prompt(
                f'  Field {i + 1} label', default='', show_default=False
            ).strip()
            if not label:
                fields.append('')
                break
            if not (NAME_MIN <= len(label) <= NAME_MAX):
                click.echo(f'  Error: label must be {NAME_MIN}–{NAME_MAX} characters.')
                continue
            fields.append(label)
            break
    return fields


def should_run_wizard(data_dir: Path) -> bool:
    """True if wizard should run: no tasks.csv AND no board key in settings.json."""
    csv_file = data_dir / 'tasks.csv'
    if csv_file.exists():
        return False
    settings_file = data_dir / 'settings.json'
    if not settings_file.exists():
        return True
    try:
        raw = json.loads(settings_file.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError):
        return True
    else:
        return 'board' not in raw


def run_setup_wizard(data_dir: Path) -> None:
    """Interactive first-run board setup wizard."""
    click.echo("Welcome to knbn! Let's configure your board.")

    active_statuses = _collect_names(
        'Active statuses, e.g., Todo, Doing, ... (columns on the board)', 2, 5
    )
    default_active = active_statuses[0]
    click.echo(f'  → Default active status: {default_active}')

    terminal_statuses = _collect_names('Terminal (done/archived) statuses', 1, 3)
    if len(terminal_statuses) == 1:
        default_terminal = terminal_statuses[0]
    else:
        click.echo('\nWhich terminal status is the default for the quick "d" key?')
        for i, s in enumerate(terminal_statuses, 1):
            click.echo(f'  ({i}) {s}')
        while True:
            idx = click.prompt('  Choice', type=int, default=1)
            if 1 <= idx <= len(terminal_statuses):
                default_terminal = terminal_statuses[idx - 1]
                break
            click.echo(f'  Please enter 1–{len(terminal_statuses)}.')

    priorities = _collect_names('Priorities (highest to lowest)', 1, 5)
    category_names = _collect_names('Categories', 1, 10)
    categories = [
        {
            'name': name,
            'color': CATEGORY_COLOR_PALETTE[i % len(CATEGORY_COLOR_PALETTE)],
        }
        for i, name in enumerate(category_names)
    ]
    free_text_fields = _collect_free_text_fields()

    board_cfg: dict = {
        'active_statuses': active_statuses,
        'default_active_status': default_active,
        'terminal_statuses': terminal_statuses,
        'default_terminal_status': default_terminal,
        'priorities': priorities,
        'categories': categories,
        'free_text_fields': free_text_fields,
    }

    data_dir.mkdir(parents=True, exist_ok=True)
    settings_file = data_dir / 'settings.json'
    existing_settings: dict = {'app': dict(SETTINGS_DEFAULTS['app']), 'board': {}}
    if settings_file.exists():
        try:
            raw = json.loads(settings_file.read_text(encoding='utf-8'))
            if isinstance(raw, dict) and 'app' in raw and isinstance(raw['app'], dict):
                existing_settings['app'].update(raw['app'])
        except (json.JSONDecodeError, OSError):
            pass
    existing_settings['board'] = board_cfg
    save_settings(data_dir, existing_settings)

    click.echo('\nBoard configuration saved.')
