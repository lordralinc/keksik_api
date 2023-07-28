import enum
import typing

__all__ = ('KeksikErrorCode', 'KeksikAPIException',)


class KeksikErrorCode(enum.IntEnum):
    UNKNOWN_METHOD = 1000
    REQUIRE_PARAMETER = 1001
    INVALID_PARAMETER = 1002
    NOT_AUTHORIZED = 1004
    INVALID_VERSION = 1005
    SERVICE_NOT_AVAILABLE = 1006
    RATE_LIMIT = 2000
    NO_ACTIVE_CAMPAIGN = 3000
    CAMPAIGN_NOT_FOUND = 3001
    OUTCOME_NOT_FOUND = 3002
    DONUT_NOT_FOUND = 3003
    LOW_BALANCE = 3004
    AMOUNT_IS_LOWER_THAN_THE_MINIMUM = 3005
    WITHDRAWAL = 3006
    API_DISABLED = 3007
    INVALID_CAMPAIGN_STOP_TIME = 3008
    AMOUNT_IS_HIGHER_THAN_THE_MAXIMUM = 3009
    PAYMENT_SYSTEM_NOT_AVAILABLE = 3010


class KeksikAPIException(Exception):
    success: typing.Literal[False] = False
    error_code: KeksikErrorCode
    message: str
    extra: typing.Dict[str, typing.Any]

    def __init__(self, **kwargs):
        self.error_code = KeksikErrorCode(kwargs.get('error', KeksikErrorCode.UNKNOWN_METHOD))
        self.message = kwargs.get('msg', 'unknown')
        self.extra = kwargs
