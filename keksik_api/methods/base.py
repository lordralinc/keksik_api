from keksik_api.base import ABCAPI

__all__ = ('BaseMethodCategory',)


class BaseMethodCategory:

    def __init__(self, api: ABCAPI):
        self.api = api
