"""Asserts that demo/settings.json and the packaged defaults are in sync."""

import json
from importlib.resources import files
from pathlib import Path


def test_defaults_board_matches_demo() -> None:
    demo_path = Path(__file__).parent.parent / 'demo' / 'settings.json'
    demo_board = json.loads(demo_path.read_text(encoding='utf-8'))['board']

    pkg_raw = (
        files('knbn').joinpath('defaults/settings.json').read_text(encoding='utf-8')
    )
    pkg_board = json.loads(pkg_raw)['board']

    assert pkg_board == demo_board, (
        'knbn/defaults/settings.json board block differs from demo/settings.json. '
        'Keep them in sync manually.'
    )
