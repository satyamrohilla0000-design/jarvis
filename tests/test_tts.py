"""Unit tests for the async speech queue. pyttsx3 is fully mocked — no audio
hardware or working TTS driver required to run these."""

from __future__ import annotations

import sys
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def _make_mock_engine() -> MagicMock:
    engine = MagicMock()
    engine.getProperty.return_value = [MagicMock(id="voice-0")]
    return engine


def test_speak_returns_immediately_and_does_not_block():
    with patch("core.speech.tts.pyttsx3") as mock_pyttsx3:
        mock_pyttsx3.init.return_value = _make_mock_engine()
        from core.speech.tts import SpeechQueue

        sq = SpeechQueue()
        start = time.monotonic()
        sq.speak("hello there")
        elapsed = time.monotonic() - start

        assert elapsed < 0.1, "speak() must return immediately, not block on TTS playback"

        sq.wait_until_done()
        sq.shutdown()


def test_queued_text_actually_gets_spoken():
    with patch("core.speech.tts.pyttsx3") as mock_pyttsx3:
        mock_engine = _make_mock_engine()
        mock_pyttsx3.init.return_value = mock_engine
        from core.speech.tts import SpeechQueue

        sq = SpeechQueue()
        sq.speak("hello there")
        sq.wait_until_done()

        mock_engine.say.assert_called_once_with("hello there")
        mock_engine.runAndWait.assert_called_once()
        sq.shutdown()


def test_fresh_engine_created_per_utterance():
    """This is the actual reliability fix: pyttsx3.init() must be called once
    per utterance, not once for the whole app — see the module docstring in
    core/speech/tts.py for why."""
    with patch("core.speech.tts.pyttsx3") as mock_pyttsx3:
        mock_pyttsx3.init.side_effect = lambda: _make_mock_engine()
        from core.speech.tts import SpeechQueue

        sq = SpeechQueue()
        sq.speak("first")
        sq.speak("second")
        sq.speak("third")
        sq.wait_until_done()

        assert mock_pyttsx3.init.call_count == 3
        sq.shutdown()


def test_empty_text_is_ignored():
    with patch("core.speech.tts.pyttsx3") as mock_pyttsx3:
        mock_engine = _make_mock_engine()
        mock_pyttsx3.init.return_value = mock_engine
        from core.speech.tts import SpeechQueue

        sq = SpeechQueue()
        sq.speak("")
        sq.wait_until_done()

        mock_engine.say.assert_not_called()
        sq.shutdown()
