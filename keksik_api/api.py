import logging
import typing

import aiohttp

from keksik_api.base import ABCAPI
from keksik_api.exceptions import KeksikAPIException
from keksik_api.methods.campaigns import CampaignsCategory
from keksik_api.methods.donates import DonatesCategory
from keksik_api.methods.payments import PaymentsCategory

__all__ = ('KeksikAPI',)

logger = logging.getLogger('keksik_api')


class KeksikAPI(ABCAPI):

    def __init__(
            self,
            group_id: int,
            access_token: str,
            api_version: typing.Literal[1] = 1,
            session: typing.Union[aiohttp.ClientSession, None] = None,
    ):
        self.group_id = group_id
        self.api_version = api_version
        self._access_token = access_token
        self._session = session

    @property
    def donates(self) -> DonatesCategory:
        return DonatesCategory(self)

    @property
    def campaigns(self) -> CampaignsCategory:
        return CampaignsCategory(self)

    @property
    def payments(self) -> PaymentsCategory:
        return PaymentsCategory(self)

    @property
    def session(self) -> aiohttp.ClientSession:
        if not self._session:
            self._session = aiohttp.ClientSession(
                base_url='https://api.keksik.io',
                headers={
                    'User-Agent': "lordralinc/keksik_api",
                    'Content-Type': 'application/json'
                }
            )
        return self._session

    def set_access_token(self, access_token: str):
        self._access_token = access_token

    async def request(
            self,
            method: str,
            params: typing.Dict[str, typing.Any],
            /,
            raise_errors: bool = True,
            clean_none: bool = True
    ) -> dict:
        if clean_none:
            params = dict({k: v for k, v in params.items() if v is not None})

        logger.debug(f"Make request to {method} with params {params}")

        params.setdefault('group', self.group_id)
        params.setdefault('token', self._access_token)
        params.setdefault('v', self.api_version)

        async with self.session.post(
                f'/{method}',
                json=params
        ) as response:
            json_response = await response.json()
            logger.debug(f"Response {method} is {json_response}")
            if json_response.get('success', False):
                return json_response
            if raise_errors:
                raise KeksikAPIException(**json_response)
            return json_response
