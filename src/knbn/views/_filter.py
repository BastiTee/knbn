"""Predicate for filtering tasks by a search query."""

from __future__ import annotations

from knbn.model.task import Task


def task_matches(task: Task, query: str) -> bool:
    """Return True if *query* is a case-insensitive substring of any searchable field."""
    if not query:
        return True
    q = query.casefold()
    return any(
        q in field.casefold()
        for field in (
            task.title,
            task.category,
            task.free_text_1,
            task.free_text_2,
            task.free_text_3,
        )
        if field
    )
