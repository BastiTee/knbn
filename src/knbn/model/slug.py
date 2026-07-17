"""Slug generation for notes filenames."""

from __future__ import annotations

import re

_MAX_SLUG_LEN = 60


def make_slug(title: str) -> str:
    slug = title.lower()
    slug = slug.replace(' ', '-')
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    slug = re.sub(r'-{2,}', '-', slug)
    slug = slug.strip('-')
    return slug[:_MAX_SLUG_LEN]


def unique_slug(title: str, existing: set[str]) -> str:
    base = make_slug(title)
    if base not in existing:
        return base
    counter = 2
    while True:
        candidate = f'{base}-{counter}'
        if candidate not in existing:
            return candidate
        counter += 1
