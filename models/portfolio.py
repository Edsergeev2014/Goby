''' Модель Portfolio '''
from assets.arguments import Description
# from tinkoff.invest.schemas import PositionsSecurities
from goby_test import Goby
from models.instruments import T_Instruments
from models.info import Info

class T_Portfolio():
    def __init__(self):
        self.description = Description()
        self.goby = Goby()
        self.instruments = T_Instruments()
        self.info = Info()
        # self.positionsecurities = PositionsSecurities()

    async def get_portfolio_positions(self):
        position_info = list()
        # Получаем список аккаунтов
        accounts = await self.info.accounts(content='list_dict') # Получаем развернутую инфо о счетах
        # print('accounts: ', accounts)
        portfolio_positions = list()
        account_positions = dict()

        # Получаем позиции для каждого аккаунта:
        for account in accounts:
            # Обнуляем список позиций для каждого аккаунта
            position_to_account_list = []
            # print('account: ', account)
            # print('account.id: ', account['id'])
            # Список позиций в аккаунте
            # positions = await self.goby.get_portfolio_positions(account_id=account.id)
            positions = await self.goby.get_portfolio_positions(account_id=account['id'])
            # print('positions в портфеле: ', positions)
            for position in positions:
                # print('position.figi: ', position.figi)
                # Данные по каждой позиции: название, цена закрытия, валюта, сектор экономики,вид инструмента (акция, валюта)
                position_info = await self.instruments.get_instruments_info(figies=position.figi)
                # print('position_info: ', position_info)
                # Добавляем данные о количестве позиции в портфеле
                position_info[-1]['balance'] = position.balance
                print('position_info: ', position_info)
                # Формируем список позиций (акций)
                position_to_account_list.append(position_info[0])

            # Формируем общий лист по позициям для каждого портфеля (аккаунта)
            account_positions = dict(account=account,
                                 positions=position_to_account_list
            # print('account_positions: ', account_positions)
            # return account_positions
                                 )
            # Полный портфель: аккаунт и его позиции (с количеством инструментов)
            portfolio_positions.append(account_positions)
            print('portfolio_positions: ', portfolio_positions)

        return portfolio_positions
