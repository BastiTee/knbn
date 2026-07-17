"""CLI commands for knbn."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import click

from knbn.config import resolve_data_dir
from knbn.model.store import add_task, ensure_data_dir
from knbn.model.task import DEFAULT_CATEGORIES, PRIORITY_VALUES, Task

_DATE_FMT = '%-B %-d, %Y %-I:%M %p'


def _now_str() -> str:
    now = datetime.now()
    return now.strftime('%B %-d, %Y %-I:%M %p')


def _prompt_select(label: str, options: list[str], default: str) -> str:
    opts_str = '  '.join(f'({i + 1}) {opt}' for i, opt in enumerate(options))
    default_idx = options.index(default) + 1
    idx: int = click.prompt(
        f'{label}\n  {opts_str}',
        type=int,
        default=default_idx,
    )
    return options[idx - 1]


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
    already_existed = data_dir.exists()
    ensure_data_dir(data_dir)
    if already_existed:
        print(f'Already initialized at {data_dir}')
    else:
        print(f'Initialized knbn data at {data_dir}')


@cli.command()
def board() -> None:
    """Launch the interactive Kanban board."""
    from knbn.app import KnbnApp  # pragma: no cover

    data_dir = resolve_data_dir()  # pragma: no cover
    ensure_data_dir(data_dir)  # pragma: no cover
    from knbn.config import get_setting  # pragma: no cover

    theme = get_setting(data_dir, 'theme', 'textual-dark')  # pragma: no cover
    KnbnApp(data_dir=data_dir, theme=theme).run()  # pragma: no cover


@cli.command()
@click.option('--title', '-t', default=None, help='Task title (skips prompt)')
@click.option('--status-default', 'status_default', is_flag=True, help='Use default status (Todo)')
@click.option('--priority-default', 'priority_default', is_flag=True, help='Use default priority (Medium)')
@click.option('--category-default', 'category_default', is_flag=True, help='Use default category (Ideas)')
@click.option('--no-resource', 'no_resource', is_flag=True, help='Skip key resource prompt')
@click.option('--fast', '-f', is_flag=True, help='Use all defaults and skip all optional prompts')
def add(
    title: str | None,
    status_default: bool,
    priority_default: bool,
    category_default: bool,
    no_resource: bool,
    fast: bool,
) -> None:
    """Quickly add a new task."""
    if fast:
        status_default = priority_default = category_default = no_resource = True

    data_dir = resolve_data_dir()
    ensure_data_dir(data_dir)

    # Title
    if title is None:
        title = click.prompt(click.style('Title', bold=True), type=str)

    # Status
    active_statuses = ['Todo', 'Now', 'Feedback', 'Delegated']
    if status_default:
        status = 'Todo'
    else:
        status = _prompt_select('Status', active_statuses, 'Todo')

    # Conditional: Feedback From
    feedback_from = ''
    if status == 'Feedback':
        feedback_from = click.prompt(click.style('Feedback From', bold=True), type=str)

    # Conditional: Delegated To
    delegated_to = ''
    if status == 'Delegated':
        delegated_to = click.prompt(click.style('Delegated To', bold=True), type=str)

    # Priority
    if priority_default:
        priority = 'Medium'
    else:
        priority = _prompt_select('Priority', PRIORITY_VALUES, 'Medium')

    # Category
    if category_default:
        category = 'Ideas'
    else:
        category = _prompt_select('Category', DEFAULT_CATEGORIES, 'Ideas')

    # Key Resource
    key_resource = ''
    if not no_resource:
        raw = click.prompt(
            click.style('Key Resource', bold=True) + ' (URL, Enter to skip)',
            default='',
        )
        key_resource = '' if raw in ('', '-') else raw

    now = _now_str()
    task = Task(
        title=title,
        category=category,
        status=status,
        priority=priority,
        date_created=now,
        date_modified=now,
        due='',
        key_resource=key_resource,
        feedback_from=feedback_from,
        delegated_to=delegated_to,
    )
    add_task(data_dir, task)
    print(f'✓ Task added: {title}')
