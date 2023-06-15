import datetime
import random
import typing

from keksik_api import schemas
from keksik_api.methods.base import BaseMethodCategory

__all__ = ('DonatesCategory',)


class DonatesCategory(BaseMethodCategory):

    async def get(
            self,
            count: typing.Optional[int] = None,
            offset: typing.Optional[int] = None,
            start_date: typing.Optional[datetime.datetime] = None,
            end_date: typing.Optional[datetime.datetime] = None,
            sort: typing.Optional[typing.Literal['date', 'amount']] = None,
            reverse: typing.Optional[bool] = None,
            **kwargs
    ) -> schemas.DonatesGetResponse:
        """Получение списка донатов

        .. warning::    У данного метода есть лимиты.
        .. warning::    Лимит составляет **100 запросов в сутки**.
            Для регулярной проверки новых донатов используйте метод `donates.get_last`.

        :param count: Количество донатов в списке. Максимум ``100``. По умолчанию ``20``.
        :param offset: Смещение по выборе донатов.
        :param start_date: Задает минимальную дату и время выбираемых донатов.
        :param end_date: Задает максимальную дату и время выбираемых донатов.
        :param sort: Метод сортировки. По умолчанию `date`.
            **Возможные значения**:
            ``date`` - сортировка по дате;
            ``amount`` - сортировка по сумме.
        :param reverse: Направление сортировки. По умолчанию ``False``.
            **Возможные значения**:
            ``False`` - сортировка по убыванию;
            ``True`` - сортировка по возрастанию.
        """
        return schemas.DonatesGetResponse.parse_obj(
            await self.api.request(
                'donates/get',
                dict(
                    count=count,
                    offset=offset,
                    start_date=int(start_date.timestamp() * 1000),
                    end_date=int(end_date.timestamp() * 1000),
                    sort=sort,
                    reverse=reverse,
                    **kwargs
                )
            )
        )

    async def get_last(self, last_id: typing.Optional[int] = None, **kwargs) -> schemas.DonatesGetResponse:
        """ Получение списка последних донатов

        .. warning:: У данного метода есть лимиты.
        .. warning:: Допускается 1 запрос в минуту.
        .. warning:: Без передачи параметра last допускается максимум 100 запрсоов в сутки.

        :param last_id: ID последнего полученного доната.
            Если данный параметр передан, вернется список с более новыми донатами.
            Если не передавать данный параметр, то вернется список последних 20 донатов.
            Таким образом вы можете при первом запросе не передав этот параметр получить актуальный список последних
            донатов, выбрать из списка самый последний донат и в следующем запросе передать ID этого доната,
            чтобы проверить наличие новых донатов.
            Если вернется пустой массив, то продолжайте передавать тот же ID.
            Как только в массиве вернется какое-то количество новых донатов, обновите ID последнего доната и в новом
            запросе передайте обновленный ID.
            Обратите внимание, что можно делать только 1 запрос в минуту.
            Для моментального оповещения о новых донатах используйте наш Callback API.
        """
        return schemas.DonatesGetResponse.parse_obj(
            await self.api.request(
                'donates/get-last',
                dict(last=last_id, **kwargs)
            )
        )

    async def change_status(
            self,
            donat_id: int,
            status: typing.Union[
                typing.Literal[schemas.DonateStatus.PUBLIC, schemas.DonateStatus.HIDDEN],
                typing.Literal['public', 'hidden']
            ],
            **kwargs
    ) -> schemas.BaseResponse:
        """Изменить статус доната

        :param donat_id: ID доната в системе.
        :param status: Статус доната.
            **Возможные значения**:
            ``public`` - опубликован;
            ``hidden`` - скрыт.
        :return:
        """
        return schemas.BaseResponse.parse_obj(
            await self.api.request(
                'donates/change-status',
                dict(id=donat_id, status=schemas.DonateStatus(status).value, **kwargs)
            )
        )

    async def answer(
            self,
            donat_id: int,
            answer: str,
            **kwargs
    ) -> schemas.BaseResponse:
        """Добавить/изменить ответ сообщества на донат

        :param donat_id: ID доната в системе.
        :param answer: Текст ответа. Для удаления ответа следует передать пустую строку.
        """
        return schemas.BaseResponse.parse_obj(
            await self.api.request(
                'donates/answer',
                dict(id=donat_id, answer=answer, **kwargs)
            )
        )

    async def change_reward_status(
            self,
            donat_id: int,
            status: typing.Union[
                schemas.RewardStatus,
                typing.Literal['not_sended', 'sended']
            ],
            **kwargs
    ) -> schemas.BaseResponse:
        """Добавить/изменить ответ сообщества на донат

        :param donat_id: ID доната в системе.
        :param status: Статус выдачи вознаграждения.
            ``not_sended`` - не выдано;
            ``sended`` - выдано.
        """
        return schemas.BaseResponse.parse_obj(
            await self.api.request(
                'donates/change-reward-status',
                dict(id=donat_id, status=status, **kwargs)
            )
        )

    @staticmethod
    def generate_op_code() -> int:
        """Сгенерировать целое положительное число, которое присваивается донату,
        при переходе пользователя по ссылке при донате.
        """
        return random.randint(1, 4294967295)

    def generate_donate_link(
            self,
            donate_sum: typing.Optional[typing.Union[int, bool]] = None,
            op_code: typing.Optional[int] = None,
            *,
            group_id: typing.Optional[int] = None,
    ) -> str:
        """Генерирует ссылку на донат

        :param donate_sum: Сумма автоподставления
        :param op_code: целое положительное число, которое присваивается донату,
            при переходе пользователя по ссылке при донате. Если указать True,
            откроется окно с вводом доната.
        :param group_id: ID группы
        :return:
        """
        group_id = group_id or self.api.group_id
        if group_id is None:
            raise ValueError("group_id is required")
        if op_code is not None:
            if op_code < 1 or op_code > 4294967295:
                raise ValueError("op_code must be in range(1, 4294967296)")
        hash_values = []
        if op_code:
            hash_values.append(f"op_{op_code}")
        if donate_sum is not None:
            if isinstance(donate_sum, bool):
                if donate_sum:
                    hash_values.append(f"donate")
            elif isinstance(donate_sum, int):
                hash_values.append(f"donate_{donate_sum}")

        return "https://vk.com/app6887721_{group_id}{hash}".format(
            group_id=-abs(group_id),
            hash="#" + "&".join(hash_values) if hash_values else ""
        )
