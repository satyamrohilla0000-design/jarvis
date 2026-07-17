"""Tests for web.py's play_song fix.

pywhatkit is mocked in sys.modules *before* import, because it transitively
imports pyautogui -> mouseinfo, which requires a real display connection at
import time. That's fine on a real desktop; this sandbox has none. Mocking
it here still exercises the actual bug fix (the string-stripping logic),
just without pywhatkit's real playback call.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.modules.setdefault("pywhatkit", MagicMock())

from core.commands.handlers.web import play_song  # noqa: E402
from core.commands.router import JarvisContext  # noqa: E402


def make_context() -> JarvisContext:
    return JarvisContext(speech=MagicMock())


def test_play_strips_leading_word_only_no_leading_space():
    ctx = make_context()
    play_song("play believer by imagine dragons", ctx)

    spoken = [call.args[0] for call in ctx.speech.speak.call_args_list]
    assert spoken[0] == "Playing believer by imagine dragons"  # no leading space


def test_play_only_strips_first_occurrence_of_the_word_play():
    # Old bug: command.replace("play", "") would strip *every* occurrence of
    # "play", not just the leading command word.
    ctx = make_context()
    play_song("play playlist songs", ctx)

    spoken = [call.args[0] for call in ctx.speech.speak.call_args_list]
    assert spoken[0] == "Playing playlist songs"


def test_play_with_no_song_name_asks_for_clarification():
    ctx = make_context()
    play_song("play", ctx)

    spoken = [call.args[0] for call in ctx.speech.speak.call_args_list]
    assert spoken == ["What would you like me to play?"]
