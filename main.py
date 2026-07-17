"""Jarvis desktop assistant — entry point.

Run with: python main.py
"""

from __future__ import annotations

import datetime
import logging

from config.settings import ASSISTANT_NAME
from core.commands.handlers import info, system, web
from core.commands.router import CommandRouter, JarvisContext
from core.speech.stt import ListenResult, SpeechListener
from core.speech.tts import SpeechQueue
from utils.logger import setup_logging

logger = logging.getLogger(__name__)


def build_router() -> CommandRouter:
    router = CommandRouter()
    web.register(router)
    system.register(router)
    info.register(router)
    return router


def wish_user(speech: SpeechQueue) -> None:
    hour = datetime.datetime.now().hour
    if hour < 12:
        greeting = "Good Morning Sir"
    elif hour < 18:
        greeting = "Good Afternoon Sir"
    else:
        greeting = "Good Evening Sir"

    speech.speak(greeting)
    speech.speak(f"I am {ASSISTANT_NAME}. How may I help you?")


def main() -> None:
    setup_logging()
    logger.info("Starting %s", ASSISTANT_NAME)

    speech = SpeechQueue()
    listener = SpeechListener()
    context = JarvisContext(speech=speech)
    router = build_router()

    wish_user(speech)

    try:
        while True:
            outcome = listener.listen()

            if outcome.status == ListenResult.OK:
                matched = router.dispatch(outcome.text, context)
                if not matched:
                    speech.speak("Sorry Sir, I did not understand")

            elif outcome.status == ListenResult.TIMEOUT:
                # Nobody said anything — not an error, stay quiet and keep listening.
                continue

            elif outcome.status == ListenResult.UNCLEAR:
                speech.speak("Sorry, I didn't catch that")

            elif outcome.status == ListenResult.NO_INTERNET:
                speech.speak("I'm having trouble reaching the internet")

            elif outcome.status == ListenResult.NO_MIC:
                speech.speak("I can't find a microphone")

    except KeyboardInterrupt:
        speech.speak("Goodbye Sir")
        speech.wait_until_done()
    finally:
        speech.shutdown()


if __name__ == "__main__":
    main()
