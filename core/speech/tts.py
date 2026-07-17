"""Text-to-speech: a background worker thread pulling from a queue.

Two problems in the original code, fixed here in one design:

1. Blocking: engine.say() + engine.runAndWait() blocks the calling thread
   until speech finishes, so the assistant can't do anything else (listen,
   track gestures, etc.) while talking. Fixed by running speech on a
   dedicated worker thread; speak() just enqueues and returns immediately.

2. Reliability: on Windows, reusing one pyttsx3 engine across many
   say()/runAndWait() cycles is a documented bug — the first call speaks
   fine, and every call after that silently produces no audio with no
   exception raised (pyttsx3 issue #419). Fixed by creating a fresh engine
   for every single utterance instead of keeping one alive for the app's
   lifetime.
"""

from __future__ import annotations

import logging
import queue
import threading

import pyttsx3

from config.settings import ASSISTANT_NAME, TTS_RATE, TTS_VOLUME, VOICE_INDEX

logger = logging.getLogger(__name__)


class SpeechQueue:
    """Non-blocking TTS. Call speak() from anywhere; a worker thread handles playback."""

    def __init__(self) -> None:
        self._queue: "queue.Queue[str]" = queue.Queue()
        self._stop_event = threading.Event()
        self._worker = threading.Thread(target=self._run, name="tts-worker", daemon=True)
        self._worker.start()

    def speak(self, text: str) -> None:
        """Queue text to be spoken. Returns immediately — never blocks the caller."""
        if not text:
            return
        print(f"{ASSISTANT_NAME}: {text}")
        logger.info("Speaking: %s", text)
        self._queue.put(text)

    def wait_until_done(self) -> None:
        """Block until everything currently queued has been spoken.

        Only meant to be used right before shutting the app down (e.g. after
        a goodbye message) — never in the normal listen/dispatch loop.
        """
        self._queue.join()

    def shutdown(self) -> None:
        """Stop the worker thread. Safe to call more than once."""
        self._stop_event.set()
        self._worker.join(timeout=2)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                text = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue
            self._speak_now(text)
            self._queue.task_done()

    def _speak_now(self, text: str) -> None:
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty("voices")
            if voices:
                index = min(VOICE_INDEX, len(voices) - 1)
                engine.setProperty("voice", voices[index].id)
            engine.setProperty("rate", TTS_RATE)
            engine.setProperty("volume", TTS_VOLUME)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception:
            logger.exception("TTS engine failed to speak: %s", text)
