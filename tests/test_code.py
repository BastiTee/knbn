"""Test suite for knbn."""

from knbn import greet


class TestGreet:
    """Tests for the greet function."""

    def test_greet_returns_greeting(self) -> None:
        """Test that greet returns a properly formatted greeting."""
        result = greet('Alice')
        assert result == 'Hello, Alice!'

    def test_greet_with_empty_string(self) -> None:
        """Test that greet handles empty string input."""
        result = greet('')
        assert result == 'Hello, !'
