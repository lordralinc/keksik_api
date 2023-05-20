import datetime
import enum
import typing

import pydantic

from keksik_api.schemas.base import BaseModel, BaseResponse


class PaymentStatus(enum.Enum):
    CREATED = 'created'
    READY = 'ready'
    ERROR = 'error'


class PaymentSystem(enum.Enum):
    BANK_CARD = 'bank-card'
    BANK_CARD_SNG = 'bank-card-sng'
    BANK_CARD_UAH = 'bank-card-uah'
    QIWI = 'qiwi'
    WEBMONEY = 'webmoney'
    YOOMONEY = 'yoomoney'
    MOBILE = 'mobile'


class Payment(BaseModel):
    id: int
    status: PaymentStatus
    processed: datetime.datetime
    system: PaymentSystem
    purse: str
    amount: int
    user_id: int = pydantic.Field(alias='user')


class PaymentsGetResponse(BaseResponse):
    items: typing.Optional[typing.List[Payment]] = pydantic.Field(None, alias='list')


class PaymentsCreateResponse(BaseResponse):
    id: typing.Optional[int] = None


class PaymentsBalanceResponse(BaseResponse):
    balance: typing.Optional[int] = None
