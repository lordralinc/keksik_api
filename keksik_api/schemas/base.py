import typing

import pydantic

from keksik_api.exceptions import KeksikErrorCode

__all__ = ('BaseModel', 'BaseResponse',)


class BaseModel(pydantic.BaseModel):

    class Config(pydantic.BaseConfig):
        frozen = True


class BaseResponse(BaseModel):
    success: typing.Literal[True] = True
    error_code: typing.Optional[KeksikErrorCode] = pydantic.Field(None, alias='error')
    message: typing.Optional[str] = pydantic.Field(None, alias='msg')
