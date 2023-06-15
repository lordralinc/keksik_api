import abc
import typing


class ABCAPI(abc.ABC):
    group_id: typing.Optional[int]

    @abc.abstractmethod
    async def request(self, method: str, params: typing.Dict[str, typing.Any], **kwargs) -> dict:
        ...

