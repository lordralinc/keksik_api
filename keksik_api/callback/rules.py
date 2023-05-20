import abc

from keksik_api import schemas

__all__ = ('Rule', 'EventTypeRule',)


class Rule(abc.ABC):

    @abc.abstractmethod
    async def check(self, event: schemas.Event) -> bool:
        ...


class EventTypeRule(Rule):

    def __init__(self, event_type: schemas.EventType):
        self.event_type = event_type

    async def check(self, event: schemas.Event) -> bool:
        return event.type == self.event_type
