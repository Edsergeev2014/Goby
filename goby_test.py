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
from tinkoff.invest.services import OperationsService
from tinkoff.invest import Quotation, MoneyValue
from tinkoff.invest import TradingDay
# from tinkoff.invest import TradingSchedule

# Загружаем режимы токенов:
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
# INVEST_GRPC_API - "боевой",
# INVEST_GRPC_API_SANDBOX - "песочница"


class Goby():
    def __init__(self):
        # self.__config = AutoConfig(search_path='assets/tsc_tokens/sandbox')
        self.__config = AutoConfig(search_path='assets/tsc_tokens/onlyread')
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
            # print('get_trading_activity: ', response)
        return response.exchanges

    async def get_trading_schedules(self, exchange: str = None):
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
        # with Client(token=self.__tsc_token) as client:
            if exchange:
                response = await client.instruments.trading_schedules(exchange=exchange)
            else:
                response = await client.instruments.trading_schedules()
        # Проверка на отсутствие совпадений для запроса
        print('response trading_schedules: ', response)
        if response.exchanges:
            response =  response.exchanges[0]
            # tradingschedule = TradingSchedule()
            # response = tradingschedule.days
            # return response.exchanges
        return response

    def trading_day(self):
        return TradingDay()


    ''' Сервис СЧЕТОВ  '''
    ''' Получить список открытых аккаунтов '''
    async def get_accounts(self):
        # x = self.test_client()
        # async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
        async with AsyncClient(token=self.__tsc_token) as client:
            response = await client.users.get_accounts()
            # print("responce: ", response)
            return response.accounts

    ''' СЕРВИС ПОРТФЕЛЯ '''
    ''' Получить информацию о позициях в портфеле '''
    async def get_portfolio_positions(self,  account_id: str = ''):
        # async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
        async with AsyncClient(token=self.__tsc_token) as client:
            response = await client.operations.get_positions(account_id=account_id)
            return response.securities  # Получаем только часть информации - Список ценно-бумажных позиций портфеля.

    ''' СЕРВИС ИНСТРУМЕНТОВ '''
    ''' Получить информацию по акции '''
    async def get_instrument_info(self, ticker='', figi=''):
        # async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
        async with AsyncClient(token=self.__tsc_token) as client:
            if figi:
                # print('figi: ', figi)
                # response = await client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id='BBG000B9XRY4')
                response = await client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)
                print("figi, response: ", response)
            elif ticker:
                # response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code='SPBXM', id='AAPL')
                response = await client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code='SPBXM', id=ticker)
                # print("ticker, response: ", response)
            else:
                print(f"Goby: Заполните данные по запросу акции: figi - {figi}, ticker - {ticker}.")
            return response.instrument if any([figi,ticker]) else None

    ''' Получить информацию по нескольким акциям '''
    async def get_instruments_info(self, tickers: list = None, figies: list = None):
        pass

    ''' Получить список всех акций: '''
    async def get_all_shares(self, instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL):
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
            response = await client.instruments.shares(instrument_status=instrument_status)
            # print("response: ", response)
            return response.instruments

    ''' Получить список любых инструментов: '''
    async def get_any_instrument(self, t_instrument='', instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL):
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
            if t_instrument == 'share': response = await client.instruments.shares(instrument_status=instrument_status)
            if t_instrument == 'currency': response = await client.instruments.currencies(instrument_status=instrument_status)
            if t_instrument == 'bond': response = await client.instruments.bonds(instrument_status=instrument_status)
            if t_instrument == 'etf': response = await client.instruments.etfs(instrument_status=instrument_status)
            if t_instrument == 'future': response = await client.instruments.futures(instrument_status=instrument_status)
            # print("response: ", response)
            return response.instruments


    ''' Запрос списка и содержания всех акций и облигаций'''
    # def getMarketStocks(self):
    #     response = self.__client.get_market_stocks()
    #     return response
    #
    # def getMarketBonds(self):
    #     response = self.__client.get_market_bonds()
    #     return response
    #
    # def getMarketByTicker(self, ticker):
    #     response = self.__client.get_market_search_by_ticker(ticker)
    #     return response

    ''' Получить цену актива '''
    async def get_market_price(self, figi='', ticker=''):
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
            # response = client.market_data.get_last_prices(figi=figi)
            if figi:
                response = await client.market_data.get_last_prices(figi=[str(figi)])
            elif ticker:
                response = await client.market_data.get_last_prices(ticker=[str(ticker)])
            else: return None
            # print("response: ", response)
            return response.last_prices

    ''' Получить свечи по инструменту '''
    async def get_stock_candles(self, figi, from_, to, interval):
        # async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
        async with AsyncClient(token=self.__tsc_token) as client:
            response = await client.market_data.get_candles(figi=figi, from_=from_, to=to, interval=interval)
            '''format: from=datetime.datetime(2021,1,1), to=datetime.datetime.now(), interval=CandleInterval.CANDLE_INTERVAL_DAY '''
            # print("response: ", response)
            return response.candles

    ''' Создаем  list-файл '''

    def createListData(self, stock_candle):
        new_row = dict()
        my_list = list()
        # print(df_stock)
        for row in stock_candle:
            ''' Проверка содержания: '''
            # print(f"time: {'{:%d %B}'.format(goby.utc_2_msc(row.time))}, "
            #       f"high: {'{:.2f}'.format(goby.price_to_float(row.high))}, "
            #       f"low: {'{:.2f}'.format(goby.price_to_float(row.low))}, "
            #       f"open: {'{:.2f}'.format(goby.price_to_float(row.open))}, "
            #       f"close: {'{:.2f}'.format(goby.price_to_float(row.close))}, "
            #       f"volume: {'{:.0f}'.format(row.volume)}, "
            #       f"is_complete: {row.is_complete} "
            #       )
            new_row = {
                "time": f'{self.utc_2_msc(row.time)}',
                # "time": datetime.datetime.strptime(row.time, '%b %d %Y %I:%M%p'),
                "high": float('{:.2f}'.format(self.price_to_float(row.high))),
                "low": float('{:.2f}'.format(self.price_to_float(row.low))),
                "open": float('{:.2f}'.format(self.price_to_float(row.open))),
                "close": float('{:.2f}'.format(self.price_to_float(row.close))),
                "volume": int('{:.0f}'.format(row.volume)),
                "is_complete": row.is_complete
            }
            # print(new_row)
            my_list.append(new_row)
            # print(my_list)
        return my_list