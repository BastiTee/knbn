"""CLI commands for knbn."""

from __future__ import annotations

from pathlib import Path

import click

from knbn.config import load_board_config, resolve_data_dir
from knbn.model.store import add_task, ensure_data_dir
from knbn.model.task import Task, now_str


def _prompt_select(label: str, options: list[str], default: str) -> str:
    opts_str = '  '.join(f'({i + 1}) {opt}' for i, opt in enumerate(options))
    default_idx = options.index(default) + 1 if default in options else 1
    while True:
        idx: int = click.prompt(
            f'{label}\n  {opts_str}',
            type=int,
            default=default_idx,
        )
        if 1 <= idx <= len(options):
            return options[idx - 1]
        click.echo(f'Please enter a number between 1 and {len(options)}.')


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    if ctx.invoked_subcommand is None:
        ctx.invoke(board)


@cli.command()
@click.argument('path', required=False)
def init(path: str | None) -> None:
    """Initialize the knbn data directory."""
    data_dir = Path(path) if path else resolve_data_dir()
    from knbn.setup import run_setup_wizard, should_run_wizard

    already_existed = data_dir.exists()
    if should_run_wizard(data_dir):
        run_setup_wizard(data_dir)
    ensure_data_dir(data_dir)
    if already_existed:
        print(f'Already initialized at {data_dir}')
    else:
        print(f'Initialized knbn data at {data_dir}')


@cli.command()
def board() -> None:
    """Launch the interactive Kanban board."""
    from knbn.app import KnbnApp  # pragma: no cover
    from knbn.config import get_app_setting  # pragma: no cover
    from knbn.setup import run_setup_wizard, should_run_wizard  # pragma: no cover

    data_dir = resolve_data_dir()  # pragma: no cover
    if should_run_wizard(data_dir):  # pragma: no cover
        run_setup_wizard(data_dir)  # pragma: no cover
    ensure_data_dir(data_dir)  # pragma: no cover
    theme = get_app_setting(data_dir, 'theme', 'textual-dark')  # pragma: no cover
    KnbnApp(data_dir=data_dir, theme=theme).run()  # pragma: no cover


@cli.command()
@click.option('--title', '-t', default=None, help='Task title (skips prompt)')
@click.option(
    '--status-default', 'status_default', is_flag=True, help='Use default status'
)
@click.option(
    '--priority-default',
    'priority_default',
    is_flag=True,
    help='Use default priority',
)
@click.option(
    '--category-default',
    'category_default',
    is_flag=True,
    help='Use default category',
)
@click.option(
    '--no-resource', 'no_resource', is_flag=True, help='Skip key resource prompt'
)
@click.option(
    '--no-free-text', 'no_free_text', is_flag=True, help='Skip free-text field prompts'
)
@click.option(
    '--fast', '-f', is_flag=True, help='Use all defaults and skip all optional prompts'
)
def add(
    title: str | None,
    status_default: bool,
    priority_default: bool,
    category_default: bool,
    no_resource: bool,
    no_free_text: bool,
    fast: bool,
) -> None:
    """Quickly add a new task."""
    if fast:
        status_default = priority_default = category_default = no_resource = (
            no_free_text
        ) = True

    data_dir = resolve_data_dir()
    ensure_data_dir(data_dir)
    board_config = load_board_config(data_dir)

    active_statuses = board_config.active_statuses
    category_names = [c.name for c in board_config.categories]
    priorities = board_config.priorities
    default_status = active_statuses[0]
    default_priority = priorities[len(priorities) // 2]
    default_category = category_names[-1] if category_names else ''

    # Title
    if title is None:
        title = click.prompt(click.style('Title', bold=True), type=str)

    # Status
    if status_default:
        status = default_status
    else:
        status = _prompt_select('Status', active_statuses, default_status)

    # Priority
    if priority_default:
        priority = default_priority
    else:
        priority = _prompt_select('Priority', priorities, default_priority)

    # Category
    if category_default:
        category = default_category
    else:
        category = _prompt_select('Category', category_names, default_category)

    # Key Resource
    key_resource = ''
    if not no_resource:
        raw = click.prompt(
            click.style('Key Resource', bold=True) + ' (URL, Enter to skip)',
            default='',
        )
        key_resource = '' if raw in ('', '-') else raw

    # Free-text fields
    free_texts: dict[str, str] = {}
    if not no_free_text:
        for i, label in board_config.active_free_text_fields():
            raw = click.prompt(
                click.style(label, bold=True) + ' (Enter to skip)',
                default='',
            )
            free_texts[f'free_text_{i + 1}'] = raw

    now = now_str()
    task = Task(
        title=title,
        category=category,
        status=status,
        priority=priority,
        date_created=now,
        date_modified=now,
        due='',
        key_resource=key_resource,
        free_text_1=free_texts.get('free_text_1', ''),
        free_text_2=free_texts.get('free_text_2', ''),
        free_text_3=free_texts.get('free_text_3', ''),
    )
    add_task(data_dir, task)
    print(f'✓ Task added: {title}')
