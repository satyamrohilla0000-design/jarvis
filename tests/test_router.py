"""Unit tests for the command router. No hardware or network required."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.commands.router import CommandRouter, JarvisContext  # noqa: E402


def make_context() -> JarvisContext:
    return JarvisContext(speech=MagicMock())


def test_dispatch_matches_registered_trigger():
    router = CommandRouter()
    calls = []
    router.add("open youtube", handler=lambda cmd, ctx: calls.append(cmd))

    matched = router.dispatch("please open youtube now", make_context())

    assert matched is True
    assert calls == ["please open youtube now"]


def test_dispatch_no_match_uses_fallback():
    router = CommandRouter()
    fallback_calls = []
    router.set_fallback(lambda cmd, ctx: fallback_calls.append(cmd))

    matched = router.dispatch("do a barrel roll", make_context())

    assert matched is False
    assert fallback_calls == ["do a barrel roll"]


def test_dispatch_no_match_and_no_fallback_returns_false():
    router = CommandRouter()
    matched = router.dispatch("anything", make_context())
    assert matched is False


def test_more_specific_trigger_wins_regardless_of_registration_order():
    """This is the fix over a plain if/elif: with an if/elif, whichever branch
    is written first wins even if a later one is a better match. Here, a
    generic "open" handler registered *before* a specific "open youtube"
    handler must not shadow it."""
    router = CommandRouter()
    order = []
    router.add("open", handler=lambda cmd, ctx: order.append("generic_open"))
    router.add("open youtube", handler=lambda cmd, ctx: order.append("specific_youtube"))

    router.dispatch("open youtube", make_context())

    assert order == ["specific_youtube"]


def test_multiple_triggers_on_one_handler():
    router = CommandRouter()
    calls = []
    router.add("exit", "stop", handler=lambda cmd, ctx: calls.append(cmd))

    router.dispatch("stop", make_context())
    router.dispatch("exit", make_context())

    assert calls == ["stop", "exit"]
