import logging
import typing

from keksik_api import schemas
from keksik_api.callback.handler import Handler
from keksik_api.callback.rules import Rule, EventTypeRule

__all__ = ('Router',)

logger = logging.getLogger('keksik_api.callback')


class Router:
    handlers: typing.List[Handler]

    def __init__(self):
        self.handlers = []

    def include_router(self, router: "Router"):
        self.handlers.extend(router.handlers)

    def on_event(
            self,
            *rules: Rule
    ):
        def decorator(
                function: typing.Callable[[schemas.Event], typing.Coroutine[typing.Any, typing.Any, typing.Any]]
        ):
            self.handlers.append(Handler(list(rules), function))
            return function

        return decorator

    def on_new_donate(self, *rules: Rule):
        def decorator(
                function: typing.Callable[[schemas.DonateEvent], typing.Coroutine[typing.Any, typing.Any, typing.Any]]
        ):
            self.handlers.append(Handler([EventTypeRule(schemas.EventType.NEW_DONATE), *rules], function))
            return function

        return decorator

    def on_payment_status(self, *rules: Rule):
        def decorator(
                function: typing.Callable[
                    [schemas.PaymentStatusEvent],
                    typing.Coroutine[typing.Any, typing.Any, typing.Any]
                ]
        ):
            self.handlers.append(Handler([EventTypeRule(schemas.EventType.PAYMENT_STATUS), *rules], function))
            return function

        return decorator

    async def route(self, event: schemas.Event):
        logger.debug(f"Process event: {event}")
        for handler in self.handlers:
            if await handler.check(event):
                await handler.handle(event)
