"""Data directory resolution."""

from __future__ import annotations

import os
from pathlib import Path

_ENV_VAR = 'KNBN_DATA_DIR'
_DEFAULT_DIR = Path.home() / '.knbn'


def resolve_data_dir() -> Path:
    env_val = os.environ.get(_ENV_VAR)
    if env_val:
        return Path(env_val)
    return _DEFAULT_DIR
