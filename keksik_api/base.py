import abc
import typing


class ABCAPI(abc.ABC):

    @abc.abstractmethod
    async def request(self, method: str, params: typing.Dict[str, typing.Any], **kwargs) -> dict:
        ...

