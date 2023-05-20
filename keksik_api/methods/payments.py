import typing

from keksik_api import schemas
from keksik_api.methods.base import BaseMethodCategory

__all__ = ('PaymentsCategory',)


class PaymentsCategory(BaseMethodCategory):

    async def get(self, ids: typing.Optional[typing.List[int]] = None, **kwargs) -> schemas.PaymentsGetResponse:
        """ Получить список заявок на выплату (последние 20 заявок).

        :param ids: Можно передать массив системных ID заявок на выплату для выборки конкретных заявок на выплату.
            Если данный параметр не передан, то вернутся 20 последних заявок на выплату.
        """
        return schemas.PaymentsGetResponse.parse_obj(
            await self.api.request(
                'payments/get',
                dict(ids=ids, **kwargs)
            )
        )

    async def create(
            self,
            system: typing.Union[
              schemas.PaymentSystem,
              typing.Literal[
                  'bank-card', 'bank-card-uah',
                  'bank-card-sng', 'qiwi', 'webmoney',
                  'yoomoney', 'mobile'
              ]
            ],
            purse: str,
            amount: int,
            name: typing.Optional[str] = None,
            **kwargs
    ) -> schemas.PaymentsCreateResponse:
        """Создать заявку на выплату.

        :param system: Платежная система.
            ``bank-card`` - Банковская карта;
            ``bank-card-uah`` - Банковская карта (UAH);
            ``bank-card-sng`` - Банковская карта (СНГ);
            ``qiwi`` - Qiwi;
            ``webmoney`` - WebMoney (только Z-кошельки);
            ``yoomoney`` - ЮMoney;
            ``mobile`` - Счет мобильного телефона.
        :param purse: Счет в платежной системе на который будет произведена выплата.
        :param amount: Сумма выплаты в рублях.
        :param name: Имя и фамилия в точности как написано на банковской карточке, на которую заказывается выплата.
            Данное поле обязательно только при выплате `bank-card-uah` и `bank-card-sng`.
        """
        return schemas.PaymentsCreateResponse.parse_obj(
            await self.api.request(
                'payments/create',
                dict(
                    system=schemas.PaymentSystem(system).value,
                    purse=purse,
                    amount=amount,
                    name=name,
                    **kwargs
                )
            )
        )

    async def balance(self, **kwargs) -> schemas.PaymentsBalanceResponse:
        """Получить баланс группы в приложении."""
        return schemas.PaymentsBalanceResponse.parse_obj(
            await self.api.request(
                'balance',
                kwargs
            )
        )
