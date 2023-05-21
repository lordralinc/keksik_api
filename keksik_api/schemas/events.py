import enum

import pydantic

from keksik_api.api import KeksikAPI
from keksik_api.schemas.donates import Donate
from keksik_api.schemas.payments import Payment

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
    api: KeksikAPI

    class Config(pydantic.BaseConfig):
        arbitrary_types_allowed = True


class DonateEvent(Event):
    donate: Donate


class PaymentStatusEvent(Event):
    payment: Payment
