import datetime
import typing

from keksik_api import schemas
from keksik_api.methods.base import BaseMethodCategory

__all__ = ('CampaignsCategory',)


class CampaignsCategory(BaseMethodCategory):

    async def get(
            self,
            ids: typing.Optional[typing.List[int]],
            **kwargs
    ) -> schemas.CampaignsGetResponse:
        """ Получить список краудфандинговых кампаний (последние 20 кампаний).

        :param ids: Можно передать массив системных ID кампаний для выборки конкрентных кампаний.
            Если данный параметр не передан, то вернутся 20 последних кампаний.
        """
        return schemas.CampaignsGetResponse.parse_obj(
            await self.api.request(
                'campaigns/get',
                dict(ids=ids, **kwargs)
            )
        )

    async def get_active(self, **kwargs) -> schemas.CampaignsGetActiveResponse:
        """Получить активную краудфандинговую кампанию."""
        return schemas.CampaignsGetActiveResponse.parse_obj(
            await self.api.request(
                'campaigns/get-active',
                dict(**kwargs)
            )
        )

    async def get_rewards(self, campaign_id: int, **kwargs) -> schemas.CampaignsGetRewardsResponse:
        """Получить список вознаграждений краудфандинговой кампании.

        :param campaign_id: ID кампании в системе.
        """
        return schemas.CampaignsGetRewardsResponse.parse_obj(
            await self.api.request(
                'campaigns/get-rewards',
                dict(campaign=campaign_id, **kwargs)
            )
        )

    async def change(
            self,
            campaign_id: int,
            title: typing.Optional[str] = None,
            status: typing.Optional[
                typing.Union[
                    schemas.CampaignStatus,
                    typing.Literal['draft', 'active', 'archive']
                ]
            ] = None,
            end: typing.Optional[datetime.datetime] = None,
            point: typing.Optional[str] = None,
            start_received: typing.Optional[str] = None,
            start_backers: typing.Optional[str] = None,
            **kwargs
    ) -> schemas.BaseResponse:
        """ Обновить информацию о краудфандинговой кампании.

        :param campaign_id: ID кампании в системе.
        :param title: Заголовок кампании.
        :param status: Статус кампании.
            ``draft`` - черновик;
            ``active`` - активная кампания;
            ``archive`` - кампания архивирована.
        :param end: Временная метка окончания кампании.
        :param point: Цель по сбору в рублях.
        :param start_received: Собрано за пределами приложения в рублях.
        :param start_backers: Кол-во спонсоров пожертвовавших за пределами приложения.
        """
        return schemas.BaseResponse.parse_obj(
            await self.api.request(
                'campaigns/change',
                dict(
                    id=campaign_id, title=title,
                    status=schemas.CampaignStatus(status).value,
                    end=int(end.timestamp() * 1000),
                    point=point,
                    start_received=start_received, start_backers=start_backers,
                    **kwargs
                )
            )
        )

    async def change_reward(
            self,
            reward_id: int,
            title: typing.Optional[str] = None,
            description: typing.Optional[str] = None,
            min_donate: typing.Optional[int] = None,
            limits: typing.Optional[int] = None,
            status: typing.Optional[
                typing.Union[
                    schemas.CampaignRewardStatus,
                    typing.Literal['public', 'hidden']
                ]
            ] = None,
            **kwargs
    ) -> schemas.BaseResponse:
        return schemas.BaseResponse.parse_obj(
            await self.api.request(
                'campaigns/change-reward',
                dict(
                    id=reward_id,
                    title=title,
                    desc=description,
                    min_donate=min_donate,
                    limits=limits,
                    status=schemas.CampaignRewardStatus(status).value,
                    **kwargs
                )
            )
        )
