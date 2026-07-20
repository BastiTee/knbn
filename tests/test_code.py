"""Smoke tests for the knbn package."""

import knbn


def test_package_has_version() -> None:
    import importlib.metadata

    version = importlib.metadata.version('knbn')
    assert version != ''


def test_cli_entry_point_importable() -> None:
    from knbn.__main__ import main

    assert callable(main)


def test_package_module_is_knbn() -> None:
    assert knbn.__name__ == 'knbn'
