# Загружаем модули Многопоточности и Ассинхронности:
import asyncio
# from threading import Thread
# Загружаем модули обработки времени и временнных зон:
import time, datetime
from pytz import timezone
# Загружаем дополнительные модули:
from decouple import AutoConfig
# Загружаем свои методы
from assets.color import color as cls
from assets.arguments import Description
# Загружаем модули Тинькофф Инвестиции
from tinkoff.invest import Account, Client, AsyncClient, OperationState, OrderDirection, OrderType, InstrumentStatus, InstrumentIdType, MarketDataRequest, InstrumentsRequest, CandleInterval
from tinkoff.invest import Quotation, MoneyValue
from tinkoff.invest import TradingDay

# Загружаем режимы токенов:
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
# INVEST_GRPC_API - "боевой",
# INVEST_GRPC_API_SANDBOX - "песочница"


class Goby():
    def __init__(self):
        self.__config = AutoConfig(search_path='assets/tsc_tokens/sandbox')
        self.__tsc_token = self.__config('TSC_TOKEN')
        self.__target = INVEST_GRPC_API_SANDBOX


    ''' Обработка аргументов. Конвертация: '''
    ''' Обработка цен '''
    def price_to_float(self, quotation):
        return float('{:.2f}'.format(quotation.units + quotation.nano / 1e9))  # nano - 9 нулей

    def price_to_quotation(self, price: float = 0):
        # import tinkoff.invest.schemas.Quotation
        # price_units = int(price)
        # price_nano = int(round(price-price_units, 2) * 1e9)
        quotation = Quotation()
        quotation.units = int(price)
        quotation.nano = int(round(price-quotation.units, 2) * 1e9)
        return quotation

    ''' Обработка стоимости '''
    def money_value_float(self, quotation):
        return float('{:.2f}'.format(quotation.units + quotation.nano/1e9)), str(quotation.currency)   # nano - 9 нулей

    def money_to_quotation(self, money: float = 0, currency: str = ''):
        # import tinkoff.invest.schemas.Quotation
        # price_units = int(price)
        # price_nano = int(round(price-price_units, 2) * 1e9)
        money_value = MoneyValue()
        # print('currency: ', currency.upper())
        money_value.currency = currency.upper()
        # print('money_value.currency: ', money_value.currency)
        money_value.units = int(money)
        money_value.nano = int(round(money-money_value.units, 2) * 1e9)
        # print('money_value: ', money_value)
        return money_value

    def units_nano_to_float(self, quotation):
        return float('{:.2f}'.format(quotation.units + quotation.nano / 1e9))  # nano - 9 нулей

    ''' Обработка времени '''
    def utc_2_msc(self, utc_time_zone):
        # Смена часового пояса на 3 часа:
        # from datetime import datetime, timezone, timedelta
        # d = datetime(2020, 1, 1, 18, tzinfo=timezone(-timedelta(hours=3)))    # https: // pandas.pydata.org / pandas - docs / stable / reference / api / pandas.to_datetime.html
        return utc_time_zone + datetime.timedelta(hours=3)

    # Получить из другой временной зоны время в МСК:
    def get_msc(self, utc, is_datetime: str=''):
        moscow = timezone('Europe/Moscow')
        if is_datetime == 'datetime': fmt = '%d.%m.%Y %H:%M'
        elif is_datetime == 'date': fmt = '%d.%m.%Y'
        elif is_datetime == 'time': fmt = '%H:%M'
        elif is_datetime == 'datetimesec': fmt = '%Y-%m-%d %H:%M:%S'
        # Формат с часовой зоной:
        else: fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        local_date_time = utc.astimezone(moscow)
        return local_date_time.strftime(fmt)

    # Получить текущее время:
    def current_datetime(self):
        return datetime.datetime.now()

    # Из строки времени получить class время по единому формату:
    # например: 2020-10-17 21:00:00
    def standart_date_time(self, datetime_string, is_datetime: str=''):
        if is_datetime == 'datetime': fmt = '%d.%m.%Y %H:%M'
        elif is_datetime == 'date': fmt = '%d.%m.%Y'
        elif is_datetime == 'time': fmt = '%H:%M'
        elif is_datetime == 'datetimesec': fmt = '%Y-%m-%d %H:%M:%S'
        # Формат с часовой зоной:
        else: fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        return datetime.datetime.strptime(datetime_string, fmt)

    ''' Расписание торгов на биржах '''

    async def get_trading_activity(self):
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
        # with Client(token=self.__tsc_token) as client:
            response = await client.instruments.trading_schedules(from_=datetime.datetime.now(),to=datetime.datetime.now())
        return response.exchanges

    async def get_trading_schedules(self):
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
        # with Client(token=self.__tsc_token) as client:
            response = await client.instruments.trading_schedules()
        return response.exchanges

    def trading_day(self):
        return TradingDay()

    # async def get_exchanges_activity(self, content: str = None, exchanges: list = None, sorted: bool = False):
    #     # response = self.get_trading_activity()
    #     response = await self.get_trading_activity()
    #     # print('get_trading_activity: ', response)
    #     # return response     # возвращает Весь список бирж
    #     description = Description()
    #     trading_day = TradingDay()
    #     # Если ответ на запрос о торговых днях бирж не пустой:
    #     if response is not None:
    #         if content == 'print':
    #             # ''' Печать Развернутого содержания отчета о счетах: '''
    #             print(cls.CYAN+'Биржи: '+cls.END)
    #             if exchanges is not None:
    #                 for exchange_info in response:
    #                     # if exchange_info.exchange == exchanges:
    #                     if exchange_info.exchange in exchanges:
    #                         print(cls.CYAN+'=>'+cls.END, exchange_info.exchange, 'Дни:', exchange_info.days, 'Начало торгов:', exchange_info.start_time, 'Завершение торгов:', exchange_info.end_time, 'Начало заявок:', exchange_info.market_order_start_time, 'Завершение заявок:', exchange_info.market_order_end_time, sep=' ')
    #             print()
    #             return
    #         elif content == 'list_dict':
    #             response_list = list()
    #             # print('response: ', response)
    #             # Выполняем: Цикл по списку бирж, формируем для каждой: exchange_info.exchange, exchange_info.days
    #             # далее: цикл по exchange_info.days - TradingDay каждой биржи.
    #             # Упаковываем в единый словарь выбранных бирж и их расписаний:
    #             if exchanges is not None:
    #                 # Перебираем все биржи из полученного списка:
    #                 for exchange_info in response:
    #                     # Если биржа из списка существует в нашем списке, получаем по ней график работы 'days':
    #                     # if exchange_info.exchange == exchanges:
    #                     if exchange_info.exchange in exchanges:
    #                         # Получаем график работы биржи:
    #                         # exchange_info cостоит из: exchange_info.exchange, exchange_info.days
    #                         trading_days_info = exchange_info.days
    #                         trading_days_info = trading_days_info[0]
    #                         # return trading_days_info[0]
    #                         exchange_data = dict(exchange=description.exchanges(exchange_info.exchange),
    #                                              day=self.get_msc(trading_days_info.date, is_datetime='date'),
    #                                              is_trading_day=trading_days_info.is_trading_day,
    #                                              start_time=self.get_msc(trading_days_info.start_time, is_datetime='time'),
    #                                              end_time=self.get_msc(trading_days_info.end_time, is_datetime='time'),
    #                                              # market_order_start_time=self.get_msc(trading_days_info.market_order_start_time, is_datetime='time'),
    #                                              # market_order_end_time=self.get_msc(trading_days_info.market_order_end_time, is_datetime='time'),
    #                                              today='Сегодня' if self.get_msc(trading_days_info.date, is_datetime='date') == self.get_msc(datetime.datetime.now(), is_datetime='date') else self.get_msc(trading_days_info.date, is_datetime='date')
    #                                              )
    #                         # print('exchange_info: ', exchange_info)
    #                         # print('exchange_data: ', exchange_data)
    #                         response_list.append(exchange_data)
    #                 # Сортируем список бирж по названию, если задано это условие:
    #                 if sorted:
    #                     # Определяем ключ для сортировки (название биржи):
    #                     def target_key(target_exchanges):
    #                         return target_exchanges['exchange']
    #                     # print("response_list: ", type(response_list), response_list)
    #                     response_list.sort(key=target_key)
    #             # print('response_list: ', response_list)
    #             return response_list
    #     else:
    #         return response

    ''' Сервис СЧЕТОВ  '''
    ''' Получить список открытых аккаунтов '''
    async def get_accounts(self):
        # x = self.test_client()
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
            response = await client.users.get_accounts()
            # print("responce: ", responce)
            return response.accounts