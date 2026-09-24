"""CLI commands for knbn."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import click

from knbn.config import load_board_config, resolve_data_dir
from knbn.model.store import (
    TaskNotFoundError,
    add_task,
    delete_task_by_id,
    ensure_data_dir,
    find_task_by_id,
    load_tasks,
    update_task_by_id,
)
from knbn.model.task import Task, now_str, parse_datetime


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


def _task_to_dict(task: Task) -> dict[str, Any]:
    return {
        'id': task.id,
        'title': task.title,
        'status': task.status,
        'priority': task.priority,
        'category': task.category,
        'due': task.due,
        'key_resource': task.key_resource,
        'free_text_1': task.free_text_1,
        'free_text_2': task.free_text_2,
        'free_text_3': task.free_text_3,
        'date_created': task.date_created,
        'date_modified': task.date_modified,
    }


@click.group(invoke_without_command=True)
@click.version_option(None, '-V', '--version', package_name='knbn', prog_name='knbn')
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
@click.option('--json', 'as_json', is_flag=True, help='Output created task as JSON')
def add(
    title: str | None,
    status_default: bool,
    priority_default: bool,
    category_default: bool,
    no_resource: bool,
    no_free_text: bool,
    fast: bool,
    as_json: bool,
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

    if title is None:
        title = click.prompt(click.style('Title', bold=True), type=str)

    if status_default:
        status = default_status
    else:
        status = _prompt_select('Status', active_statuses, default_status)

    if priority_default:
        priority = default_priority
    else:
        priority = _prompt_select('Priority', priorities, default_priority)

    if category_default:
        category = default_category
    else:
        category = _prompt_select('Category', category_names, default_category)

    key_resource = ''
    if not no_resource:
        raw = click.prompt(
            click.style('Key Resource', bold=True) + ' (URL, Enter to skip)',
            default='',
        )
        key_resource = '' if raw in ('', '-') else raw

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
    saved = add_task(data_dir, task)
    if as_json:
        print(json.dumps(_task_to_dict(saved)))
    else:
        print(f'✓ Task added: {title}')


@cli.command(name='list')
@click.option('--status', '-s', multiple=True, help='Filter by status (repeatable)')
@click.option('--priority', '-p', multiple=True, help='Filter by priority (repeatable)')
@click.option('--category', '-c', multiple=True, help='Filter by category (repeatable)')
@click.option('--all', 'show_all', is_flag=True, help='Include terminal-status tasks')
@click.option(
    '--after',
    'after_date',
    default=None,
    help='Show only tasks modified on or after DATE (YYYY-MM-DD or YYYY-MM-DD HH:MM)',
)
@click.option('--json', 'as_json', is_flag=True, help='Output as JSON array')
def list_tasks(
    status: tuple[str, ...],
    priority: tuple[str, ...],
    category: tuple[str, ...],
    show_all: bool,
    after_date: str | None,
    as_json: bool,
) -> None:
    """List tasks."""
    from datetime import datetime

    after_dt: datetime | None = None
    if after_date is not None:
        parsed = parse_datetime(after_date)
        if parsed is None:
            raise click.BadParameter(
                f"'{after_date}' is not a recognised date. "
                'Use YYYY-MM-DD or YYYY-MM-DD HH:MM.',
                param_hint='--after',
            )
        after_dt, _ = parsed

    data_dir = resolve_data_dir()
    ensure_data_dir(data_dir)
    board_config = load_board_config(data_dir)
    tasks = load_tasks(data_dir)

    if not show_all:
        active = set(board_config.active_statuses)
        tasks = [t for t in tasks if t.status in active]
    if status:
        s = {v.lower() for v in status}
        tasks = [t for t in tasks if t.status.lower() in s]
    if priority:
        p_set = {v.lower() for v in priority}
        tasks = [t for t in tasks if t.priority.lower() in p_set]
    if category:
        c_set = {v.lower() for v in category}
        tasks = [t for t in tasks if t.category.lower() in c_set]
    if after_dt is not None:
        tasks = [
            t
            for t in tasks
            if (r := parse_datetime(t.date_modified)) is not None and r[0] >= after_dt
        ]

    status_order = {s: i for i, s in enumerate(board_config.all_statuses())}
    priority_order = {pr: i for i, pr in enumerate(board_config.priorities)}
    tasks.sort(
        key=lambda t: (
            status_order.get(t.status, 999),
            priority_order.get(t.priority, 999),
            t.title,
        )
    )

    if as_json:
        print(json.dumps([_task_to_dict(t) for t in tasks]))
        return

    if not tasks:
        return

    id_w = 8
    status_w = max((len(t.status) for t in tasks), default=8)
    priority_w = max((len(t.priority) for t in tasks), default=8)
    category_w = max((len(t.category) for t in tasks), default=8)
    title_w = max((len(t.title) for t in tasks), default=20)
    fmt = (
        f'{{:<{id_w}}}  {{:<{status_w}}}  {{:<{priority_w}}}  {{:<{category_w}}}  {{}}'
    )
    print(fmt.format('ID', 'Status', 'Priority', 'Category', 'Title'))
    print(
        fmt.format(
            '-' * id_w,
            '-' * status_w,
            '-' * priority_w,
            '-' * category_w,
            '-' * min(title_w, 60),
        )
    )
    for t in tasks:
        print(fmt.format(t.id, t.status, t.priority, t.category, t.title))


@cli.command()
@click.argument('task_id')
@click.option('--title', default=None, help='New title')
@click.option('--status', default=None, help='New status')
@click.option('--priority', default=None, help='New priority')
@click.option('--category', default=None, help='New category')
@click.option(
    '--due', default=None, help='New due date (YYYY-MM-DD or YYYY-MM-DD HH:MM)'
)
@click.option(
    '--key-resource', 'key_resource', default=None, help='New key resource URL'
)
@click.option('--free-text-1', 'free_text_1', default=None)
@click.option('--free-text-2', 'free_text_2', default=None)
@click.option('--free-text-3', 'free_text_3', default=None)
@click.option('--json', 'as_json', is_flag=True, help='Output updated task as JSON')
def edit(
    task_id: str,
    title: str | None,
    status: str | None,
    priority: str | None,
    category: str | None,
    due: str | None,
    key_resource: str | None,
    free_text_1: str | None,
    free_text_2: str | None,
    free_text_3: str | None,
    as_json: bool,
) -> None:
    """Edit an existing task by ID."""
    from dataclasses import replace

    all_fields = [
        title,
        status,
        priority,
        category,
        due,
        key_resource,
        free_text_1,
        free_text_2,
        free_text_3,
    ]
    if all(f is None for f in all_fields):
        raise click.UsageError('At least one field flag must be provided.')

    data_dir = resolve_data_dir()
    board_config = load_board_config(data_dir)

    try:
        task = find_task_by_id(data_dir, task_id)
    except TaskNotFoundError:
        raise click.ClickException(f"Task '{task_id}' not found")

    if status is not None and status not in board_config.all_statuses():
        valid = ', '.join(board_config.all_statuses())
        raise click.ClickException(f"Invalid status '{status}'. Valid: {valid}")
    if priority is not None and priority not in board_config.priorities:
        valid = ', '.join(board_config.priorities)
        raise click.ClickException(f"Invalid priority '{priority}'. Valid: {valid}")
    if category is not None and category not in [
        c.name for c in board_config.categories
    ]:
        valid = ', '.join(c.name for c in board_config.categories)
        raise click.ClickException(f"Invalid category '{category}'. Valid: {valid}")

    updated = replace(
        task,
        title=title if title is not None else task.title,
        status=status if status is not None else task.status,
        priority=priority if priority is not None else task.priority,
        category=category if category is not None else task.category,
        due=due if due is not None else task.due,
        key_resource=key_resource if key_resource is not None else task.key_resource,
        free_text_1=free_text_1 if free_text_1 is not None else task.free_text_1,
        free_text_2=free_text_2 if free_text_2 is not None else task.free_text_2,
        free_text_3=free_text_3 if free_text_3 is not None else task.free_text_3,
        date_modified=now_str(),
    )
    update_task_by_id(data_dir, task_id, updated)

    if as_json:
        print(json.dumps(_task_to_dict(updated)))
    else:
        print(f'✓ Task updated: {updated.title}')


@cli.command()
@click.argument('task_id')
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation prompt')
def delete(task_id: str, yes: bool) -> None:
    """Delete a task by ID."""
    data_dir = resolve_data_dir()

    try:
        task = find_task_by_id(data_dir, task_id)
    except TaskNotFoundError:
        raise click.ClickException(f"Task '{task_id}' not found")

    if not yes:
        confirmed = click.confirm(f'Delete task "{task.title}"?', default=False)
        if not confirmed:
            return

    delete_task_by_id(data_dir, task_id)
    print(f'✓ Task deleted: {task.title}')


@cli.command()
def config() -> None:
    """Show the resolved board configuration as JSON."""
    from knbn.config import load_settings

    data_dir = resolve_data_dir()
    ensure_data_dir(data_dir)
    board_config = load_board_config(data_dir)
    settings = load_settings(data_dir)
    output: dict[str, Any] = {
        'active_statuses': board_config.active_statuses,
        'default_active_status': board_config.default_active_status,
        'terminal_statuses': board_config.terminal_statuses,
        'default_terminal_status': board_config.default_terminal_status,
        'priorities': board_config.priorities,
        'categories': [
            {'name': c.name, 'color': c.color} for c in board_config.categories
        ],
        'free_text_fields': board_config.free_text_fields,
        'data_dir': str(data_dir),
        'db_version': settings.get('db_version', ''),
    }
    print(json.dumps(output, indent=2))
