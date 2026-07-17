"""Tests for slug generation."""

from knbn.model.slug import make_slug, unique_slug


def test_basic_slug() -> None:
    assert make_slug('Research feedback models') == 'research-feedback-models'


def test_lowercase() -> None:
    assert make_slug('Hello World') == 'hello-world'


def test_special_chars_stripped() -> None:
    assert make_slug('Fix bug: 360° review') == 'fix-bug-360-review'


def test_special_chars_stripped_ampersand() -> None:
    assert make_slug('Sync on Q&A planning') == 'sync-on-qa-planning'


def test_consecutive_hyphens_collapsed() -> None:
    slug = make_slug('Hello  --  World')
    assert '--' not in slug


def test_truncation_at_60_chars() -> None:
    long_title = 'a' * 70
    assert len(make_slug(long_title)) == 60


def test_truncation_preserves_content() -> None:
    title = 'word ' * 20
    assert len(make_slug(title)) <= 60


def test_no_collision() -> None:
    assert unique_slug('Research feedback models', set()) == 'research-feedback-models'


def test_collision_suffix_2() -> None:
    existing = {'research-feedback-models'}
    assert (
        unique_slug('Research feedback models', existing)
        == 'research-feedback-models-2'
    )


def test_collision_suffix_3() -> None:
    existing = {'research-feedback-models', 'research-feedback-models-2'}
    assert (
        unique_slug('Research feedback models', existing)
        == 'research-feedback-models-3'
    )


def test_unique_slug_no_existing() -> None:
    result = unique_slug('My Task', set())
    assert result == 'my-task'
