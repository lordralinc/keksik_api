import datetime
import enum
import typing

import pydantic

from keksik_api.schemas.base import BaseModel, BaseResponse

__all__ = (
    'RewardStatus',
    'Reward',
    'DonateStatus',
    'Donate',
    'DonatesGetResponse',
)


class RewardStatus(enum.Enum):
    NOT_SENDED = 'not_sended'
    SENDED = 'sended'


class Reward(BaseModel):
    id: int
    title: str
    status: RewardStatus


class DonateStatus(enum.Enum):
    NEW = 'new'
    PUBLIC = 'public'
    HIDDEN = 'hidden'


class Donate(BaseModel):
    id: int
    user_id: int = pydantic.Field(alias='user')
    date: datetime.datetime
    amount: int
    total: typing.Optional[int] = None
    message: typing.Optional[str] = pydantic.Field(None, alias='msg')
    is_anonymous: bool = pydantic.Field(alias='anonym')
    answer: typing.Optional[str] = None
    vkpay: bool
    status: DonateStatus
    reward: typing.Optional[Reward] = None
    op: typing.Optional[int] = None


class DonatesGetResponse(BaseResponse):
    items: typing.Optional[typing.List[Donate]] = pydantic.Field(None, alias='list')
