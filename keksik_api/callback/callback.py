import hashlib
import logging
import typing

from keksik_api.api import KeksikAPI
from keksik_api.schemas.events import EventType, Event, DonateEvent, PaymentStatusEvent
from keksik_api.callback.router import Router

__all__ = ('Callback',)

logger = logging.getLogger('keksik_api.callback')


class Callback:

    def __init__(
            self,
            api: KeksikAPI,
            secret_key: str,
            confirmation_code: str,
            router: typing.Optional[Router] = None
    ):
        self.api = api
        self.router = router or Router()
        self._secret_key = secret_key
        self._confirmation_code = confirmation_code
        self._application = None

    def check_hash(self, params: dict) -> bool:
        hash_value = params['hash']
        del params['hash']
        params = self.get_hash_dict(params)
        params = dict(sorted(params.items()))
        params_values = list(params.values())
        params_values.append(self._secret_key)
        hash_str = ','.join([
            ("1" if value else "") if isinstance(value, bool) else
            str(value) if not isinstance(value, str) else
            value
            for value in params_values
        ])
        sha256 = hashlib.sha256(hash_str.encode()).hexdigest()
        return sha256 == hash_value

    def get_hash_dict(self, params: dict, index: str = ''):
        hash_dict = {}
        if index:
            index += '/'
        for key, val in params.items():
            if isinstance(val, dict):
                new_dict = self.get_hash_dict(val, index + key)
                hash_dict.update(new_dict)
            else:
                hash_dict[index + key] = val
        return hash_dict

    async def route_web_request(self, event: dict) -> dict:
        logger.debug(f"New event: {event}")
        if not self.check_hash(event.copy()):
            return {"status": "error", "msg": "Invalid hash"}
        if event.get('type') == 'confirmation':
            if event.get('group') != str(self.api.group_id):
                return {"status": "error", "msg": "Invalid group id"}
            return {"status": "ok", "code": self._confirmation_code}

        type_to_dataclass = {
            EventType.NEW_DONATE.value: DonateEvent,
            EventType.PAYMENT_STATUS.value: PaymentStatusEvent,
        }
        if event.get('type') not in type_to_dataclass:
            dataclass = Event
        else:
            dataclass = type_to_dataclass[event['type']]
        await self.router.route(dataclass.parse_obj({**event, "api": self.api}))
        return {"status": "ok"}
