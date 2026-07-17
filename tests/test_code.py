"""Tests for knbn package (smoke tests)."""

from knbn import __doc__ as knbn_doc


def test_package_importable() -> None:
    assert knbn_doc is not None
