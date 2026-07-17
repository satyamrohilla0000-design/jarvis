"""Command router: matches recognized speech to a registered handler.

Replaces the old if/elif chain in execute_command(). Handlers register one
or more trigger phrases; dispatch() picks the handler whose matching
trigger is the *longest* (most specific), not just the first one
registered. That matters once the command list grows toward Phase 10's
~50 commands — a generic "open" handler and a specific "open youtube"
handler can coexist safely regardless of which one was registered first.
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Callable, Optional, Protocol

logger = logging.getLogger(__name__)


class SpeechQueueLike(Protocol):
    """Structural type for what a handler is allowed to do with speech, so this
    module doesn't need a hard import-time dependency on the concrete SpeechQueue class."""

    def speak(self, text: str) -> None: ...
    def wait_until_done(self) -> None: ...


@dataclass
class JarvisContext:
    """Shared dependencies handed to every handler. Extend this, not the function signature,
    when Phase 8 (memory) or later phases need to give handlers more to work with."""

    speech: SpeechQueueLike


CommandHandler = Callable[[str, JarvisContext], None]


@dataclass
class Route:
    triggers: tuple[str, ...]
    handler: CommandHandler
    name: str


class CommandRouter:
    def __init__(self) -> None:
        self._routes: list[Route] = []
        self._fallback: Optional[CommandHandler] = None

    def add(self, *triggers: str, handler: CommandHandler, name: Optional[str] = None) -> None:
        """Register a handler for one or more trigger phrases."""
        self._routes.append(
            Route(triggers=triggers, handler=handler, name=name or handler.__name__)
        )

    def set_fallback(self, handler: CommandHandler) -> None:
        self._fallback = handler

    def dispatch(self, command: str, context: JarvisContext) -> bool:
        """Run the handler whose matching trigger is most specific. Returns True if anything matched."""
        best_route: Optional[Route] = None
        best_len = -1

        for route in self._routes:
            for trigger in route.triggers:
                if trigger in command and len(trigger) > best_len:
                    best_route = route
                    best_len = len(trigger)

        if best_route is not None:
            logger.info("Routed %r -> %s", command, best_route.name)
            best_route.handler(command, context)
            return True

        if self._fallback is not None:
            self._fallback(command, context)
        return False
