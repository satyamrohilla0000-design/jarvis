"""Handlers for informational commands: time, Wikipedia lookups."""

from __future__ import annotations

import datetime
import logging

import wikipedia

from core.commands.router import CommandRouter, JarvisContext

logger = logging.getLogger(__name__)

_WIKI_PREFIXES = ("who is", "what is", "who was", "what was")


def tell_time(command: str, ctx: JarvisContext) -> None:
    now = datetime.datetime.now().strftime("%I:%M %p")
    ctx.speech.speak(f"The time is {now}")


def wikipedia_search(command: str, ctx: JarvisContext) -> None:
    # Original bug: the *entire* command (e.g. "who is elon musk") was
    # passed straight into wikipedia.summary() instead of just the topic
    # ("elon musk"), which hurt hit rate. Strip the question prefix first.
    query = command
    for prefix in _WIKI_PREFIXES:
        if command.startswith(prefix):
            query = command[len(prefix):].strip()
            break

    if not query:
        ctx.speech.speak("Who or what would you like to know about?")
        return

    ctx.speech.speak("Searching Wikipedia")
    try:
        result = wikipedia.summary(query, sentences=2)
        ctx.speech.speak(result)
    except wikipedia.exceptions.DisambiguationError as exc:
        options = ", ".join(exc.options[:3])
        ctx.speech.speak(f"That could mean a few things, including {options}. Could you be more specific?")
    except wikipedia.exceptions.PageError:
        ctx.speech.speak(f"Sorry, I couldn't find anything about {query}")
    except Exception:
        logger.exception("Wikipedia lookup failed for query: %s", query)
        ctx.speech.speak("Sorry, I could not find information on that")


def register(router: CommandRouter) -> None:
    router.add("time", handler=tell_time)
    router.add(*_WIKI_PREFIXES, handler=wikipedia_search)
