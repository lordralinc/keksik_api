import datetime
import enum
import typing

import pydantic

from keksik_api.schemas.base import BaseModel, BaseResponse

__all__ = (
    'CampaignStatus',
    'Campaign',
    'CampaignsGetResponse',
    'CampaignsGetActiveResponse',
    'CampaignRewardStatus',
    'CampaignReward',
    'CampaignsGetRewardsResponse',
)


class CampaignStatus(enum.Enum):
    DRAFT = 'draft'
    ACTIVE = 'active'
    ARCHIVE = 'archive'


class Campaign(BaseModel):
    id: int
    title: str
    status: CampaignStatus
    start: datetime.datetime
    end: datetime.datetime
    point: int
    start_received: int
    start_backers: int
    received: int
    backers: int


class CampaignsGetResponse(BaseResponse):
    items: typing.Optional[typing.List[Campaign]] = pydantic.Field(None, alias='list')


class CampaignsGetActiveResponse(BaseResponse):
    campaign: typing.Optional[Campaign]


class CampaignRewardStatus(enum.Enum):
    PUBLIC = 'public'
    HIDDEN = 'hidden'


class CampaignReward(BaseModel):
    id: int
    title: str
    description: str = pydantic.Field(alias='desc')
    min_donate: int
    limits: typing.Optional[int] = None
    status: CampaignRewardStatus
    backers: int


class CampaignsGetRewardsResponse(BaseResponse):
    items: typing.Optional[typing.List[CampaignReward]] = pydantic.Field(None, alias='list')
