import enum
import typing

import pydantic

from .donates import Donate
from .payments import Payment

if typing.TYPE_CHECKING:
    from keksik_api import KeksikAPI

__all__ = (
    'EventType',
    'Event',
    'DonateEvent',
    'PaymentStatusEvent',
)


class EventType(enum.Enum):
    CONFIRMATION = 'confirmation'
    NEW_DONATE = 'new_donate'
    PAYMENT_STATUS = 'payment_status'


class Event(pydantic.BaseModel):
    group_id: int = pydantic.Field(alias='group')
    type: EventType
    hash: str
    api: "KeksikAPI"


class DonateEvent(Event):
    donate: Donate


class PaymentStatusEvent(Event):
    payment: Payment
