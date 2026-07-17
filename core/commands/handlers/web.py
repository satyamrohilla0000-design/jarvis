"""Handlers for opening websites and playing media."""

from __future__ import annotations

import logging
import webbrowser



from config.settings import CHATGPT_URL, GOOGLE_URL, YOUTUBE_URL
from core.commands.router import CommandRouter, JarvisContext

logger = logging.getLogger(__name__)


def open_youtube(command: str, ctx: JarvisContext) -> None:
    ctx.speech.speak("Opening YouTube")
    webbrowser.open(YOUTUBE_URL)


def open_google(command: str, ctx: JarvisContext) -> None:
    ctx.speech.speak("Opening Google")
    webbrowser.open(GOOGLE_URL)


def open_chatgpt(command: str, ctx: JarvisContext) -> None:
    ctx.speech.speak("Opening ChatGPT")
    webbrowser.open(CHATGPT_URL)


def play_song(command: str, ctx: JarvisContext) -> None:
    # count=1 fixes two bugs in the original: a leading space left behind
    # by replace("play", ""), and "play" being stripped from anywhere in
    # the phrase rather than just the leading word.
    song = command.replace("play", "", 1).strip()
    if not song:
        ctx.speech.speak("What would you like me to play?")
        return

    ctx.speech.speak(f"Playing {song}")
    try:
        pywhatkit.playonyt(song)
    except Exception:
        logger.exception("pywhatkit failed to play: %s", song)
        ctx.speech.speak("Sorry, I couldn't play that")


def register(router: CommandRouter) -> None:
    router.add("open youtube", handler=open_youtube)
    router.add("open google", handler=open_google)
    router.add("open chat gpt", "open chatgpt", handler=open_chatgpt)
    router.add("play", handler=play_song)
