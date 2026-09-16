"""Tests for KnbnApp theme preview/persist/revert behavior."""

from __future__ import annotations

import asyncio
from pathlib import Path

from textual.widgets import OptionList

from knbn.app import KnbnApp
from knbn.config import load_settings


def test_theme_preview_flag_suppresses_persistence(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = KnbnApp(data_dir=tmp_path, theme='textual-dark')
        async with app.run_test(size=(120, 40)):
            app._theme_preview_active = True
            app.theme = 'nord'
            app._theme_preview_active = False

            assert app.theme == 'nord'
            settings = load_settings(tmp_path)
            assert settings['app']['theme'] == 'textual-dark'

    asyncio.run(scenario())


def test_selecting_highlighted_theme_persists(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = KnbnApp(data_dir=tmp_path, theme='textual-dark')
        async with app.run_test(size=(120, 40)) as pilot:
            app.action_change_theme()
            await pilot.pause(0.2)
            await pilot.press('down')
            await pilot.pause(0.2)

            previewed_theme = app.theme
            assert previewed_theme != 'textual-dark'
            settings = load_settings(tmp_path)
            assert settings['app']['theme'] == 'textual-dark'

            await pilot.press('enter')
            await pilot.pause(0.2)

            assert app.theme == previewed_theme
            settings = load_settings(tmp_path)
            assert settings['app']['theme'] == previewed_theme

    asyncio.run(scenario())


def test_theme_sidebar_docks_to_the_right_and_does_not_fill_the_window(
    tmp_path: Path,
) -> None:
    async def scenario() -> None:
        app = KnbnApp(data_dir=tmp_path, theme='textual-dark')
        async with app.run_test(size=(120, 40)) as pilot:
            app.action_change_theme()
            await pilot.pause(0.2)

            option_list = app.screen.query_one(OptionList)
            assert option_list.region.width < app.size.width
            assert option_list.region.x > 0

    asyncio.run(scenario())


def test_theme_sidebar_leaves_the_board_visible_behind_it(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = KnbnApp(data_dir=tmp_path, theme='textual-dark')
        async with app.run_test(size=(120, 40)) as pilot:
            await pilot.pause(0.2)
            app.action_change_theme()
            await pilot.pause(0.2)

            svg = app.export_screenshot()
            assert 'Kanban' in svg
            assert 'Todo' in svg

    asyncio.run(scenario())


def test_cancelling_sidebar_reverts_preview(tmp_path: Path) -> None:
    async def scenario() -> None:
        app = KnbnApp(data_dir=tmp_path, theme='textual-dark')
        async with app.run_test(size=(120, 40)) as pilot:
            app.action_change_theme()
            await pilot.pause(0.2)
            await pilot.press('down')
            await pilot.pause(0.2)

            assert app.theme != 'textual-dark'

            await pilot.press('escape')
            await pilot.pause(0.2)

            assert app.theme == 'textual-dark'
            settings = load_settings(tmp_path)
            assert settings['app']['theme'] == 'textual-dark'

    asyncio.run(scenario())
