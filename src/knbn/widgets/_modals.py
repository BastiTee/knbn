"""Simple modal dialogs for prompt and selection."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label


class PromptModal(ModalScreen[str | None]):
    """Single-line text prompt modal."""

    BINDINGS = [Binding('escape', 'cancel', 'Cancel')]

    DEFAULT_CSS = """
    PromptModal { align: center middle; }
    PromptModal > Vertical {
        background: $surface; border: round $primary;
        padding: 1 3; width: 50; height: auto;
    }
    """

    def __init__(self, prompt: str, **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._prompt_text = prompt

    def compose(self) -> ComposeResult:
        from textual.containers import Vertical

        with Vertical():
            yield Label(self._prompt_text)
            yield Input(id='prompt-input')
            yield Button('OK', id='ok-btn', variant='primary')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'ok-btn':
            inp = self.query_one('#prompt-input', Input)
            self.dismiss(inp.value.strip() or None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value.strip() or None)

    def action_cancel(self) -> None:
        self.dismiss(None)


class SelectModal(ModalScreen[str | None]):
    """Numbered selection modal."""

    BINDINGS = [Binding('escape', 'cancel', 'Cancel')]

    DEFAULT_CSS = """
    SelectModal { align: center middle; }
    SelectModal > Vertical {
        background: $surface; border: round $primary;
        padding: 1 3; width: 40; height: auto;
    }
    """

    def __init__(self, title: str, options: list[str], **kwargs: object) -> None:
        super().__init__(**kwargs)  # type: ignore[arg-type]
        self._select_title = title
        self._options = options

    def compose(self) -> ComposeResult:
        from textual.containers import Vertical

        with Vertical():
            yield Label(self._select_title)
            for i, opt in enumerate(self._options, 1):
                yield Button(f'({i}) {opt}', id=f'opt-{i}')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id and event.button.id.startswith('opt-'):
            idx = int(event.button.id.split('-')[1]) - 1
            self.dismiss(self._options[idx])

    def action_cancel(self) -> None:
        self.dismiss(None)
