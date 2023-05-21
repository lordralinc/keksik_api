import typing

from keksik_api import schemas
from keksik_api.callback.rules import Rule

__all__ = ('Handler',)


class Handler:
    rules: typing.List[Rule]
    handler: typing.Callable[[schemas.Event], typing.Coroutine[typing.Any, typing.Any, typing.Any]]

    def __init__(
            self,
            rules: typing.List[Rule],
            handler: typing.Callable[[schemas.Event], typing.Coroutine[typing.Any, typing.Any, typing.Any]]
    ):
        self.rules = rules
        self.handler = handler

    async def check(self, event: schemas.Event) -> bool:
        for rule in self.rules:
            if not await rule.check(event):
                return False
        return True

    async def handle(self, event: schemas.Event):
        return await self.handler(event)

    def __repr__(self):
        return f"Handler({self.handler.__name__}, rules={self.rules})"
