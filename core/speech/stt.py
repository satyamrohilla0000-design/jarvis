"""Speech-to-text: microphone capture + Google's free web speech API.

Fixes vs. the original take_command():
- Ambient noise calibration now runs once at startup, not on every loop
  (was costing a full extra second per command).
- recognizer.listen() now has a timeout and phrase_time_limit, so a quiet
  mic can no longer hang the app indefinitely.
- The one broad `except Exception: print(e)` is replaced with specific
  exceptions, returned as a typed ListenOutcome, so the caller can give
  different spoken feedback for "didn't catch that" vs. "no internet" vs.
  "no microphone" instead of going silent in every case.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
import logging

import speech_recognition as sr

from config.settings import AMBIENT_NOISE_DURATION, STT_PHRASE_TIME_LIMIT, STT_TIMEOUT

logger = logging.getLogger(__name__)


class ListenResult(Enum):
    OK = auto()
    TIMEOUT = auto()  # nothing was said — not an error, just silence
    UNCLEAR = auto()  # speech was heard but not understood
    NO_INTERNET = auto()  # Google's STT API couldn't be reached
    NO_MIC = auto()  # no working microphone found


@dataclass
class ListenOutcome:
    status: ListenResult
    text: str = ""


class SpeechListener:
    """Wraps a Recognizer + Microphone. Calibrates ambient noise once, then listens on demand."""

    def __init__(self) -> None:
        self._recognizer = sr.Recognizer()
        self._calibrated = False

    def listen(self) -> ListenOutcome:
        try:
            with sr.Microphone() as source:
                if not self._calibrated:
                    logger.info("Calibrating microphone for ambient noise...")
                    self._recognizer.adjust_for_ambient_noise(
                        source, duration=AMBIENT_NOISE_DURATION
                    )
                    self._calibrated = True

                try:
                    audio = self._recognizer.listen(
                        source, timeout=STT_TIMEOUT, phrase_time_limit=STT_PHRASE_TIME_LIMIT
                    )
                except sr.WaitTimeoutError:
                    return ListenOutcome(ListenResult.TIMEOUT)

        except OSError:
            logger.exception("No microphone available")
            return ListenOutcome(ListenResult.NO_MIC)

        try:
            command = self._recognizer.recognize_google(audio).lower()
            logger.info("Heard: %s", command)
            return ListenOutcome(ListenResult.OK, command)
        except sr.UnknownValueError:
            return ListenOutcome(ListenResult.UNCLEAR)
        except sr.RequestError:
            logger.exception("Speech API request failed")
            return ListenOutcome(ListenResult.NO_INTERNET)
