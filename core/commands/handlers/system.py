"""Handlers for system-level commands: launching local apps, exiting."""

from __future__ import annotations

import logging
import os
import sys

from config.settings import VS_CODE_PATH
from core.commands.router import CommandRouter, JarvisContext

logger = logging.getLogger(__name__)


def open_vscode(command: str, ctx: JarvisContext) -> None:
    # This was the one confirmed bug from the brief: the original branch
    # called os.startfile() but never spoke anything.
    ctx.speech.speak("Opening VS Code")
    try:
        os.startfile(VS_CODE_PATH)
    except FileNotFoundError:
        logger.error("VS Code path not found: %s", VS_CODE_PATH)
        ctx.speech.speak("I couldn't find that project folder. Check the path in settings.")
    except OSError:
        logger.exception("Failed to open VS Code path: %s", VS_CODE_PATH)
        ctx.speech.speak("Something went wrong opening that")


def exit_app(command: str, ctx: JarvisContext) -> None:
    ctx.speech.speak("Goodbye Sir")
    ctx.speech.wait_until_done()  # make sure "Goodbye" is actually spoken before the process dies
    sys.exit(0)


def register(router: CommandRouter) -> None:
    router.add("open code", handler=open_vscode)
    router.add("exit", "stop", handler=exit_app)
