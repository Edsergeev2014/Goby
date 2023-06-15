#
import asyncio
from threading import Thread

# from tinkoff.invest.sandbox.client import Client
from tinkoff.invest import Account, Client, AsyncClient, CloseSandboxAccountResponse, MoneyValue, OperationState, OrderDirection, OrderType, InstrumentStatus, InstrumentIdType, MarketDataRequest, InstrumentsRequest, CandleInterval
from tinkoff.invest import OperationType, TradingDay
from tinkoff.invest import RequestError as error
from tinkoff.invest import Quotation
from tinkoff.invest import PortfolioRequest
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
# INVEST_GRPC_API - "боевой",
# INVEST_GRPC_API_SANDBOX - "песочница"
from decouple import AutoConfig

import time, datetime
import pytz
from pytz import timezone
import locale
# устанавливаем локаль
# locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))   # выдаёт ошибку, ранее работал
locale.setlocale(locale.LC_ALL)
import pandas as pd
import json
import matplotlib.pyplot as plt
import mplfinance as mpf

from assets.color import color as cls
from assets.arguments import Description


class AsyncLoopThread(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.loop = asyncio.new_event_loop()
    def run(self) -> None:
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

class Goby():
    def __init__(self):
        self.__config = AutoConfig(search_path='assets/tsc_tokens/sandbox')
        self.__tsc_token = self.__config('TSC_TOKEN')
        self.__target = INVEST_GRPC_API_SANDBOX

        # self.__client = tinvest.SyncClient(self.__tsc_token, use_sandbox=True)
        # self.__client = self.sandbox_service()

        self.stock_name = ''                    #   Название акции
        self.isNextOperationBuy = True          #   Какая следующая операция доступна
        self.upWard_Trend_Threshold = 1.5       #   Уровень цены, выше которой считать трендом вверх
        self.dip_Threshold = - 2.25             #   Уровень цены, ниже которой считать трендом вниз
        self.profit_Threshold = 1.25            #   Take-profit
        self.stop_Loss_Threshold = - 2.00       #   Stock_loss

        self.lastOpPrice = 100.00

    # ''' Проверка токена '''
    # def getToken(self):
    #     return self.__tsc_token

    def my_generator(self, iter=int()):
        for i in range(iter):
            yield i

    async def get_trading_activity(self):
        async with Client(token=self.__tsc_token, target=self.__target) as client:
        # with Client(token=self.__tsc_token) as client:
            response = await client.instruments.trading_schedules(from_=datetime.datetime.now(),to=datetime.datetime.now())
        return response.exchanges

    async def get_exchanges_activity(self, content: str = None, exchanges: list = None):
        # response = self.get_trading_activity()
        response = await self.get_trading_activity()
        # print('get_trading_activity: ', response)
        # return response     # возвращает Весь список бирж
        description = Description()
        trading_day = TradingDay()
        # Если ответ на запрос о торговых днях бирж не пустой:
        if response is not None:
            if content == 'print':
                # ''' Печать Развернутого содержания отчета о счетах: '''
                print(cls.CYAN+'Биржи: '+cls.END)
                if exchanges is not None:
                    for exchange_info in response:
                        # if exchange_info.exchange == exchanges:
                        if exchange_info.exchange in exchanges:
                            print(cls.CYAN+'=>'+cls.END, exchange_info.exchange, 'Дни:', exchange_info.days, 'Начало торгов:', exchange_info.start_time, 'Завершение торгов:', exchange_info.end_time, 'Начало заявок:', exchange_info.market_order_start_time, 'Завершение заявок:', exchange_info.market_order_end_time, sep=' ')
                print()
                return
            elif content == 'list_dict':
                response_list = list()
                # print('response: ', response)
                # Выполняем: Цикл по списку бирж, формируем для каждой: exchange_info.exchange, exchange_info.days
                # далее: цикл по exchange_info.days - TradingDay каждой биржи.
                # Упаковываем в единый словарь выбранных бирж и их расписаний:
                if exchanges is not None:
                    # Перебираем все биржи из полученного списка:
                    for exchange_info in response:
                        # Если биржа из списка существует в нашем списке, получаем по ней график работы 'days':
                        # if exchange_info.exchange == exchanges:
                        if exchange_info.exchange in exchanges:
                            # Получаем график работы биржи:
                            # exchange_info cостоит из: exchange_info.exchange, exchange_info.days
                            trading_days_info = exchange_info.days
                            trading_days_info = trading_days_info[0]
                            # return trading_days_info[0]
                            exchange_data = dict(exchange=description.exchanges(exchange_info.exchange),
                                                 day=self.get_msc(trading_days_info.date, is_datetime='date'),
                                                 is_trading_day=trading_days_info.is_trading_day,
                                                 start_time=self.get_msc(trading_days_info.start_time, is_datetime='time'),
                                                 end_time=self.get_msc(trading_days_info.end_time, is_datetime='time'),
                                                 market_order_start_time=self.get_msc(trading_days_info.market_order_start_time, is_datetime='time'),
                                                 market_order_end_time=self.get_msc(trading_days_info.market_order_end_time, is_datetime='time'),
                                                 today='Сегодня' if self.get_msc(trading_days_info.date, is_datetime='date') == self.get_msc(datetime.datetime.now(), is_datetime='date') else self.get_msc(trading_days_info.date, is_datetime='date')
                                                 )
                            # print('exchange_info: ', exchange_info)
                            # print('exchange_data: ', exchange_data)
                            response_list.append(exchange_data)
                # print('response_list: ', response_list)
                return response_list
        else:
            return response

    ''' Сервис СЧЕТОВ  '''
    # def sandbox_service(self):
    #     with Client(token=self.__tsc_token) as client:
    #         yield client.sandbox
    ''' Получить список открытых аккаунтов '''
    async def get_snb_accounts(self):
        # x = self.test_client()
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
            response = await client.users.get_accounts()
            # print("responce: ", responce)
            return response.accounts
    # ''' Открыть аккаунт '''
    # def open_snb_account(self):
    #     with Client(token=self.__tsc_token) as client:
    #         response = client.sandbox.open_sandbox_account()
    #         return response.account_id
    # ''' Закрыть аккаунт '''
    # async def close_snb_account(self, account_id):
    #     async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
    #         client.sandbox.close_sandbox_account(account_id=account_id)
    #         return
    # ''' Пополнить баланс счета: '''
    # def top_up_account(self, account_id, money:float=0, currency:str=''):
    #     with Client(token=self.__tsc_token) as client:
    #         return client.sandbox.sandbox_pay_in(account_id=account_id, amount=self.money_to_quotation(money=money, currency=currency))

    async def get_accounts(self, content: str = None):
        response = await self.get_snb_accounts()
        # print('get_accounts: ', response)
        description = Description()
        if response is not None:
            if content == 'print':
                # ''' Печать Развернутого содержания отчета о счетах: '''
                print(cls.CYAN+'Счета: '+cls.END)
                for account in response:
                    print(cls.CYAN+'=>'+cls.END, account.id, 'Название счёта:', account.name, 'Статус:', account.status, account.type, sep=' ')
                print()
                return
            elif content == 'list_dict':
                response_list = list()
                # print('response.accounts: ', response.accounts)
                for account in response:
                    account_info = dict(id=account.id,
                                        name=account.name,
                                        status=description.account_status(account.status),
                                        type=account.type)
                    # print('account: ', account)
                    # print('account_info: ', account_info)
                    response_list.append(account_info)
                # print('response_list: ', response_list)
                return response_list
        else:
            return response

        return

    ''' Получить информацию по акции '''
    # def get_instrument_info(self, ticker='', figi=''):
    #     with Client(token=self.__tsc_token) as client:
    #         if figi:
    #             # response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id='BBG000B9XRY4')
    #             response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)
    #         if ticker:
    #             # response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code='SPBXM', id='AAPL')
    #             response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code='SPBXM', id=ticker)
    #         # print("response: ", response)
    #         else:
    #             print("Заполните данные по запросу акции")
    #         return response.instrument

    ''' Получить информацию по нескольким акциям '''
    # def get_instruments_info(self, tickers: list = None, figies: list = None):
    #     with Client(token=self.__tsc_token) as client:
    #         response_list = list()
    #         description = Description()
    #
    #         if tickers is not None:
    #             for ticker in tickers:
    #                 if figies is None: figies = list()
    #                 figies.append(self.figi(ticker=ticker))
    #             # Другие варианты запросов через ticker:
    #             # response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code=self.class_code(ticker=ticker), id=ticker)
    #             # response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code=self.class_code(ticker=ticker), id=ticker)
    #             # response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code='SPBXM', id=ticker)
    #             # response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code='SPBXM', id='AAPL')
    #
    #         if figies is not None:
    #             for figi in figies:
    #                 response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id=figi)
    #                 # response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id='BBG000B9XRY4')
    #                 instrument_data = response.instrument
    #                 # print('instrument_data: ', instrument_data)
    #                 # Цены на начало дня и на текущее время:
    #                 # print('datetime.datetime.today(): ', datetime.date.today())
    #                 # Кол-во дней на графике
    #                 days_for_chart = int(7)
    #                 from_ = datetime.datetime.now() - datetime.timedelta(days=days_for_chart*3)
    #                 # from_ = datetime.datetime(2022, 2, 20)
    #                 # print('from_: ', from_)
    #                 instrument_candles = self.get_stock_candles(figi=instrument_data.figi,
    #                                                             from_=from_,
    #                                                             to=datetime.datetime.now(),
    #                                                             interval=5)  # CANDLE_INTERVAL_DAY - '5' - 1 день.
    #                 # print('instrument_candles: ', len(instrument_candles), instrument_candles)
    #                 # Если недостаточно данных - увеличиваем число дней для запроса
    #                 if len(instrument_candles) < days_for_chart:
    #                     from_ = datetime.datetime.now() - datetime.timedelta(days=days_for_chart * 10)
    #                     instrument_candles = self.get_stock_candles(figi=instrument_data.figi,
    #                                                                 from_=from_,
    #                                                                 to=datetime.datetime.now(),
    #                                                                 interval=5)  # CANDLE_INTERVAL_DAY - '5' - 1 день.
    #
    #                 list_data = self.createListData(instrument_candles)
    #                 # print("list_data[0]['open']: ", list_data[0]['open'])
    #                 # print("list_data[-1]['close']", list_data[-1]['close'])
    #                 open_price = list_data[-1]['open']
    #                 close_price = list_data[-1]['close']
    #                 last_7days_prices = list()
    #                 # Собираем последние цены:
    #                 for i in range(days_for_chart, 0, -1):
    #                     # print('i=', i, f'list_data[{-i}]["close"]: ', list_data[-i]['close'])
    #                     last_7days_prices.append(list_data[-i]['close'])
    #
    #                 # print('last_7days_prices: ', last_7days_prices)
    #                 # last_7days_prices = [list_data[days_for_chart*(-1)]['close'], list_data[days_for_chart*(-1)+1]['close'], list_data[days_for_chart*(-1)+2]['close'],
    #                 #                     list_data[days_for_chart*(-1)+3]['close'], list_data[days_for_chart*(-1)+4]['close'], list_data[days_for_chart*(-1)+5]['close'], list_data[days_for_chart*(-1)+6]['close']
    #                 #                     ]
    #                 green = "rgba(50,205,50,1)"     # Цвет графика
    #                 red = "rgba(220,20,60,1)"
    #                 instrument_info = dict(figi=instrument_data.figi, ticker=instrument_data.ticker,
    #                                        class_code=instrument_data.class_code,
    #                                        name=instrument_data.name,
    #                                        sector=instrument_data.sector.capitalize(),
    #                                        # last_price=self.get_last_price(instrument_data.figi),
    #                                        open_price=open_price,
    #                                        close_price=close_price,
    #                                        last_7days_prices=last_7days_prices,
    #                                        green_or_red=green if last_7days_prices[-1] > last_7days_prices[0] else red,     # Цвет графика
    #                                        currency=description.currency_type(instrument_data.currency, flag='simbol'),
    #                                        exchange=instrument_data.exchange,
    #                                        trading_status=description.trading_status(instrument_data.trading_status),
    #                                        buy_available_flag=instrument_data.buy_available_flag,
    #                                        sell_available_flag=instrument_data.sell_available_flag,
    #                                        api_trade_available_flag=instrument_data.api_trade_available_flag,
    #                                        difference=round(close_price-open_price, 2),
    #                                        percent=round((close_price-open_price)/open_price*100, 2)
    #                                        )
    #                 response_list.append(instrument_info)
    #         # print("response_list: ", response_list)
    #         else:
    #             print("Заполните данные по запросу акции")
    #         return response_list

    ''' Получить список всех акций: '''
    # def get_all_shares(self, instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL):
    #     with Client(token=self.__tsc_token) as client:
    #         response = client.instruments.shares(instrument_status=instrument_status)
    #         # print("response: ", response)
    #         return response.instruments

    ''' Получить список любых инструментов: '''
    # def get_any_instrument(self, instrument='', instrument_status=InstrumentStatus.INSTRUMENT_STATUS_ALL):
    #     with Client(token=self.__tsc_token) as client:
    #         if instrument == 'share': response = client.instruments.shares(instrument_status=instrument_status)
    #         if instrument == 'currency': response = client.instruments.currencies(instrument_status=instrument_status)
    #         if instrument == 'bond': response = client.instruments.bonds(instrument_status=instrument_status)
    #         if instrument == 'etf': response = client.instruments.etfs(instrument_status=instrument_status)
    #         if instrument == 'future': response = client.instruments.futures(instrument_status=instrument_status)
    #         # print("response: ", response)
    #         return response.instruments

    ''' Получить последнюю цену инструмента '''
    # def get_last_prices(self):
    #     with Client(token=self.__tsc_token) as client:
    #         response = client.market_data.get_last_prices()
    #         # print("response: ", response)
    #         return response.last_prices
    #
    # def get_last_price(self, figi=''):
    #     with Client(token=self.__tsc_token) as client:
    #         # response = client.market_data.get_last_prices(figi=figi)
    #         response = client.market_data.get_last_prices(figi=[str(figi)])
    #         # print("response: ", response)
    #         return response.last_prices

    ''' Получить свечи по инструменту '''
    # def get_stock_candles(self, figi, from_, to, interval):
    #     with Client(token=self.__tsc_token) as client:
    #         response = client.market_data.get_candles(figi=figi, from_=from_, to=to, interval=interval)
    #         '''format: from=datetime.datetime(2021,1,1), to=datetime.datetime.now(), interval=CandleInterval.CANDLE_INTERVAL_DAY '''
    #         # print("response: ", response)
    #         return response.candles


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

    def get_msc(self, utc, is_datetime: str=''):
        moscow = timezone('Europe/Moscow')
        if is_datetime == 'datetime': fmt = '%d.%m.%Y %H:%M'
        elif is_datetime == 'date': fmt = '%d.%m.%Y'
        elif is_datetime == 'time': fmt = '%H:%M'
        else: fmt = '%Y-%M-%d %H:%M:%S %Z%z'
        local_date_time = utc.astimezone(moscow)
        return local_date_time.strftime(fmt)

    def current_datetime(self):
        return datetime.datetime.now()



    ''' Обработка инструментов '''
    # см. arguments.py

    ''' Запрос содержания портфеля '''
    # def get_portfolio(self, account_id):
    #     with Client(token=self.__tsc_token) as client:
    #         # см. расшифровку портфеля по частям - в getBalance()
    #         return client.sandbox.get_sandbox_portfolio(account_id=account_id)

    ''' Запрос основных статей портфеля '''
    # def get_portfolio_articles(self, account_id):
    #     portfolio = self.get_portfolio(account_id=account_id)
    #     print('portfolio: ', portfolio)
    #     description = Description()
    #     if portfolio is not None:
    #         portfolio_articles = dict()
    #         if self.money_value_float(portfolio.total_amount_shares)[0] != 0: portfolio_articles = dict(Акции=[self.money_value_float(portfolio.total_amount_shares)[0], description.currency_type(self.money_value_float(portfolio.total_amount_shares)[1], 'val')])
    #         if self.money_value_float(portfolio.total_amount_bonds)[0] != 0: portfolio_articles.update(Облигации=[self.money_value_float(portfolio.total_amount_bonds)[0], description.currency_type(self.money_value_float(portfolio.total_amount_bonds)[1], 'val')])
    #         if self.money_value_float(portfolio.total_amount_etf)[0] != 0: portfolio_articles.update(ETF=[self.money_value_float(portfolio.total_amount_etf)[0], description.currency_type(self.money_value_float(portfolio.total_amount_etf)[1], 'val')])
    #         if self.money_value_float(portfolio.total_amount_currencies)[0] != 0: portfolio_articles.update(Валюты=[self.money_value_float(portfolio.total_amount_currencies)[0], description.currency_type(self.money_value_float(portfolio.total_amount_currencies)[1], 'val')])
    #         if self.money_value_float(portfolio.total_amount_futures)[0] != 0: portfolio_articles.update(Фьючерсы=[self.money_value_float(portfolio.total_amount_futures)[0], description.currency_type(self.money_value_float(portfolio.total_amount_futures)[1], 'val')])
    #         return portfolio_articles
    #     else: return

        # portfolio_articles.update('Акции': self.money_value_float(portfolio.total_amount_shares) if portfolio.total_amount_shares > 0
        #     dict({['Акции': self.money_value_float(portfolio.total_amount_shares) if portfolio.total_amount_shares > 0],
        #     'Облигации': self.money_value_float(portfolio.total_amount_bonds),
        #     'ETF': self.money_value_float(portfolio.total_amount_etf),
        #     'Валюты': self.money_value_float(portfolio.total_amount_currencies),
        #     'Фьючерсы': self.money_value_float(portfolio.total_amount_futures)
        #     })
        #     return dict({['Акции': self.money_value_float(portfolio.total_amount_shares) if portfolio.total_amount_shares > 0],
        #                  'Облигации': self.money_value_float(portfolio.total_amount_bonds),
        #                  'ETF': self.money_value_float(portfolio.total_amount_etf),
        #                  'Валюты': self.money_value_float(portfolio.total_amount_currencies),
        #                  'Фьючерсы': self.money_value_float(portfolio.total_amount_futures)
        #                  })
        # else: return


    ''' Запрос баланса портфеля '''
    # см. решение здесь:
    # https: // github.com / Tinkoff / invest - python / blob / main / examples / porfolio_stream_client.py
    # def get_balance(self, account_id):
    #
    #     portfolio = self.get_portfolio(account_id=account_id)
    #     # print('Portfolio: ', type(portfolio), portfolio)
    #     # print('Список позиций портфеля: ', portfolio.positions)
    #     description = Description()
    #
    #     # Формируем состав портфеля со стоимостью в валютах:
    #     total_value_rub, total_value_usd, total_value_eur = float(), float(), float()
    #     if portfolio is not None:
    #         portfolio_includes = dict({'shares': self.money_value_float(portfolio.total_amount_shares),
    #                                    'bonds': self.money_value_float(portfolio.total_amount_bonds),
    #                                    'etf': self.money_value_float(portfolio.total_amount_etf),
    #                                    'currencies': self.money_value_float(portfolio.total_amount_currencies),
    #                                    'futures': self.money_value_float(portfolio.total_amount_futures)
    #                                    })
    #         # Проверка данных:
    #         # print('portfolio_includes: ', portfolio_includes)
    #         # Пример вывода печати: Акции: (0.0, 'rub')
    #         # total_value_rub = {print(position,value) for (position,value) in portfolio_includes.items() if value[1] == 'rub'}
    #         # print(f'Состав портфеля, в т.ч.:  \n'
    #         #       f'Акции: {portfolio_includes["shares"]}, \n'
    #         #       f'Облигации: {portfolio_includes["bonds"]}, \n'
    #         #       f'Валюты: {portfolio_includes["currencies"]}.')
    #
    #         ''' Собираем данные портфеля в разрезе (по фильтру) валют: rub, usd, eur: '''
    #         total_value_rub = sum([value for (value, currency) in portfolio_includes.values() if currency.upper() == 'rub'.upper()])
    #         total_value_usd = sum([value for (value, currency) in portfolio_includes.values() if currency.upper() == 'usd'.upper()])
    #         total_value_eur = sum([value for (value, currency) in portfolio_includes.values() if currency.upper() == 'eur'.upper()])
    #
    #         # print('Суммы по разделам портфеля: total_value_rub: ', total_value_rub, '; total_value_usd: ', total_value_usd, '; total_value_eur: ', total_value_eur)
    #         # if total_value_rub == 0: print('total_value_rub: ', type(total_value_rub), total_value_rub)
    #         # elif total_value_usd: print('total_value_usd: ', type(total_value_usd), total_value_usd)
    #         # elif total_value_eur: print('total_value_eur: ', type(total_value_eur), total_value_eur)
    #         # else: print('Портфель - пуст')
    #
    #
    #
    #     # Возвращаем портфель со стоимостью инструментов по 3-м валютам: rub, usd, eur
    #     return dict({description.currency_type(currency_type='rub', capitalize=True): round(total_value_rub, 2),
    #                  description.currency_type(currency_type='usd', capitalize=True): round(total_value_usd, 2),
    #                  description.currency_type(currency_type='eur', capitalize=True): round(total_value_eur, 2)})

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
    # async def get_market_price(self, figi=''):
    #     async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
    #         # response = client.market_data.get_last_prices(figi=figi)
    #         response = await client.market_data.get_last_prices(figi=[str(figi)])
    #         # print("response: ", response)
    #         return response.last_prices

    ''' Метод для обвертывания запросов по операциям и позициям: '''
    def request_blank(self, account_id: str='', from_=datetime.datetime.now()-datetime.timedelta(weeks=4), to=datetime.datetime.now(),
                      state=None, figi=None):
        # state:
        # OPERATION_STATE_UNSPECIFIED     0        Статус операции не определён
        # OPERATION_STATE_EXECUTED        1        Исполнена
        # OPERATION_STATE_CANCELED        2        Отменена
        return {
            "account_id": account_id,
            "from_":from_,
            "to":to,
            # "state":state,
            # "figi":figi
        }

    ''' Метод для обвертывания запросов по ордерам: '''
    def order(self, figi: str = "", quantity: int = None, price: float = 0, direction: str = "", account_id: str='', order_type: str = "", order_id: str = ""):
        if direction == 'BUY': set_direction = OrderDirection.ORDER_DIRECTION_BUY
        elif direction == 'SELL': set_direction = OrderDirection.ORDER_DIRECTION_SELL
        else: set_direction = OrderDirection.ORDER_DIRECTION_UNSPECIFIED

        if order_type == 'MARKET': set_order_type = OrderType.ORDER_TYPE_MARKET
        elif order_type == 'LIMIT': set_order_type = OrderType.ORDER_TYPE_LIMIT
        else: set_order_type = OrderType.ORDER_TYPE_UNSPECIFIED

        return {
            "figi": "BBG000B9XRY4",
            "quantity": quantity,
            "price": price,
            "direction": set_direction,
            "account_id": account_id,
            "order_type": set_order_type,
            "order_id": order_id
        }

    # async def place_my_order(self, order):
    #     async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
    #         response = client.sandbox.post_sandbox_order(**order)
    #         print(response)
    #         return response

    ''' Разместить ордер (шаблон) '''
    # async def place_order(self, figi: str = "", quantity: int = None, price: float = 0, direction: str = "", account_id: str = "", order_type: str = "", order_id: str = ""):
    #     async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
    #         '''
    #         price: Optional[units=0, nano=0],
    #         direction: ORDER_DIRECTION_BUY - 1, ORDER_DIRECTION_SELL - 2;
    #         order_type: ORDER_TYPE_LIMIT - 1, ORDER_TYPE_MARKET - 2.
    #         '''
    #         order = self.order(figi, quantity, price, direction, account_id, order_type, order_id)
    #         return client.sandbox.post_sandbox_order(**order)

    ''' Разместить ордер на продажу '''
    # def placeSellLimitOrder(self, figi: str = "", quantity: int = None, price=dict(units=None, nano=None), account_id: str = "", order_type: str = "", order_id: str = ""):
    #     return self.place_order(self, figi=figi, quantity=quantity, price=price, direction="ORDER_DIRECTION_SELL", account_id=account_id, order_type = "ORDER_TYPE_LIMIT", order_id=order_id)
    ''' Разместить ордер на покупку '''
    # def placeBuyLimitOrder(self, figi: str = "", quantity: int = None, price=dict(units=None, nano=None), account_id: str = "", order_type: str = "", order_id: str = ""):
    #     return self.place_order(self, figi=figi, quantity=quantity, price=price, direction="ORDER_DIRECTION_BUY", account_id=account_id, order_type = "ORDER_TYPE_LIMIT", order_id=order_id)

    ''' Запрос списка ордеров: '''
    # def get_orders(self, request, content: str = None):
    #     with Client(token=self.__tsc_token) as client:
    #         # print("self.order['account_id']: ", type(order), order)
    #         # print("request_blank['account_id']: ", type(request['account_id']), request['account_id'])
    #         response = client.sandbox.get_sandbox_orders(account_id=request['account_id'])
    #         description = Description()
    #         if content == 'print':
    #             # ''' Печать Развернутого содержания отчета операций: '''
    #             print(cls.CYAN+'Поручения (ордера): '+cls.END)
    #             for order in response.orders:
    #                 print(cls.CYAN+'=>'+cls.END, order.order_date, 'Статус ордера:', order.execution_report_status, order.figi, order.direction, 'Кол-во запрошено: ', order.lots_requested, 'Кол-во исполнено: ', order.lots_executed, 'Цена исполнения: ', self.money_value_float(order.average_position_price), order.currency, 'Сумма: ', self.money_value_float(order.total_order_amount), ', в т.ч. комиссия: ', self.money_value_float(order.executed_commission), 'ID ордера: ', order.order_id, sep=' ')
    #             print()
    #             return
    #         elif content == 'list_dict':
    #             response_list = list()
    #             # print('response.orders: ', response.orders)
    #             for order in response.orders:
    #                 order_info = dict(date=self.get_msc(order.order_date, 'datetime'),
    #                                   status=description.orders_execution_report_status(order.execution_report_status),
    #                                   figi= self.name(order.figi),
    #                                   direction=description.order_direction(order.direction),
    #                                   lots_requested=str(order.lots_requested), lots_executed=str(order.lots_executed),
    #                                   average_position_price=self.money_value_float(order.average_position_price),
    #                                   currency=description.currency_type(order.currency, 'val'),
    #                                   total_order_amount = self.money_value_float(order.total_order_amount),
    #                                   executed_commission=float(self.money_value_float(order.executed_commission)[0]),
    #                                   order_id=order.order_id)
    #                 # print('order: ', order)
    #                 # print('order_info: ', order_info)
    #                 response_list.append(order_info)
    #             # print('response_list: ', response_list)
    #             return response_list
    #         else:
    #             # ''' Краткое содержание отчета поручений: '''
    #             return response

    # def order_cancel(self, request, content: str=None):
    # # def order_cancel(self, account_id: str = None, order_id: str = None, content: str = None):
    #     print('order_cancel.request: ', request['account_id'], request['order_id'])
    #     with Client(token=self.__tsc_token) as client:
    #         response = client.sandbox.cancel_sandbox_order(**request)
    #         # response = client.sandbox.cancel_sandbox_order(self.order(account_id, order_id))
    #         if content:
    #             if response.time:
    #                print(cls.YELLOW + '=> Заявка отменена.' + cls.END, 'Время исполнения:', response.time)
    #             else:
    #                print(cls.RED + '=> Запрос на отмену заявки не выполнен.' + cls.END)
    #         return response

    ''' Запрос списка позиций в портфеле: '''
    # def get_portfolio_positions(self, request, content: str=None):
    #     with Client(token=self.__tsc_token) as client:
    #         response = client.sandbox.get_sandbox_portfolio(account_id=request['account_id'])
    #         description = Description()
    #         if content == 'print':
    #             # ''' Печать Развернутого содержания отчета позиций: '''
    #             print(cls.CYAN+'Позиции портфеля: '+cls.END)
    #             for position in response.positions:
    #                 # print(position)
    #                 quantity_position = int(self.units_nano_to_float(position.quantity))
    #                 price_position = self.money_value_float(position.average_position_price)[0]
    #                 print(cls.CYAN+'=>'+cls.END, position.instrument_type, self.ticker(position.figi), 'Кол-во: ', quantity_position, 'Цена в портфеле: ', price_position, 'Цена текущая на бирже: ', self.money_value_float(position.current_price), 'Сумма: ', price_position * quantity_position, sep=' ')
    #             print()
    #             return
    #         elif content == 'list_dict':
    #             response_list = list()
    #             # print('response.orders: ', response.orders)
    #             for position in response.positions:
    #                 # print('position: ', position)
    #                 quantity_position = int(self.units_nano_to_float(position.quantity))
    #                 price_position = self.money_value_float(position.average_position_price)[0]
    #                 position_info = dict(
    #                                      # instrument_type=position.instrument_type,
    #                                      instrument_type=description.instrument_type(instrument_type=position.instrument_type, capitalize=True),
    #                                      ticker=self.name(position.figi),
    #                                      quantity_position=str(quantity_position), price_position=price_position,
    #                                      current_price=self.money_value_float(position.current_price),
    #                                      settlement_price=(round(price_position/quantity_position,2)) if quantity_position != 0 else '')
    #                 # print('position_info: ', position_info)
    #                 response_list.append(position_info)
    #             # print('response_list: ', response_list)
    #             return response_list
    #         else:
    #             # ''' Краткое содержание отчета позиций: '''
    #             return response

    ''' Запрос списка позиций: '''
    # def get_positions(self, request, content: str = None):
    #     with Client(token=self.__tsc_token) as client:
    #         response = client.sandbox.get_sandbox_positions(account_id=request['account_id'])
    #         if content:
    #             # ''' Печать Развернутого содержания отчета позиций: '''
    #             print(cls.CYAN+'Позиции: '+cls.END)
    #             for operation in response.securities:
    #                 print(operation.date, operation.instrument_type, operation.figi, operation.operation_type, 'Кол-во: ', operation.quantity, 'Цена: ', self.money_value_float(operation.price), 'Сумма: ', self.money_value_float(operation.payment), operation.currency, sep=' ')
    #             print()
    #         # ''' Краткое содержание отчета позиций: '''
    #         return response

    ''' Запрос операций: '''
    # def get_operations(self, request, content: str = None):
    #     with Client(token=self.__tsc_token) as client:
    #         response = client.sandbox.get_sandbox_operations(**request)
    #         description = Description()
    #         if content == 'print':
    #             # ''' Печать Развернутого содержания отчета операций: '''
    #             print(cls.CYAN+'Операции: '+cls.END)
    #             for operation in response.operations:
    #                 print( )
    #                 print(cls.CYAN+'=>'+cls.END, operation.date, operation.instrument_type, self.ticker(operation.figi), operation.operation_type, 'Кол-во: ', operation.quantity, 'Цена: ', self.money_value_float(operation.price), 'Сумма: ', self.money_value_float(operation.payment), operation.currency, sep=' ')
    #                 # print('operation: ', operation)
    #             return
    #         elif content == 'list_dict':
    #             response_list = list()
    #             # print('response.orders: ', response.orders)
    #             for operation in response.operations:
    #                 # print('operation: ', operation)
    #                 operation_info = dict(date=self.get_msc(operation.date, 'date'),
    #                                       instrument_type=description.instrument_type(instrument_type=operation.instrument_type, capitalize=False),
    #                                       # instrument_type=operation.instrument_type,
    #                                       ticker=self.name(operation.figi),
    #                                       operation_type=description.operation_type_description(argument=operation.operation_type),
    #                                       # operation_type={'operation.operation_type': operation.operation_type, 'operation': OperationType(operation.operation_type)},
    #                                       quantity=str(operation.quantity), price=self.money_value_float(operation.price),
    #                                       payment=self.money_value_float(operation.payment),
    #                                       currency=description.currency_type(operation.currency, 'val') if not operation.figi else description.currency_type(self.currency(operation.figi), 'val'),
    #                                       # currency=description.currency_type(operation.currency, 'val')
    #                                       )
    #                 # print('operation_info: ', operation_info)
    #                 response_list.append(operation_info)
    #             # print('response_list: ', response_list)
    #             return response_list
    #         else:
    #             # ''' Краткое содержание отчета операций: '''
    #             return response


    ''' Получить детализацию по операции '''
    def getOperationDetails(self):
        return

    ''' Покупка актива '''
    # def tryToBuy(self, percentageDiff):
    #     if percentageDiff >= self.upWard_Trend_Threshold or percentageDiff <= self.dip_Threshold:
    #         self.lastOpPrice = self.placeBuyOrder()
    #         self.isNextOperationBuy = False

    ''' Продажа актива '''
    # def tryToSell(self, percentageDiff):
    #     if percentageDiff >= self.upWard_Trend_Threshold or percentageDiff <= self.dip_Threshold:
    #         self.lastOpPrice = self.placeSellOrder()
    #         self.isNextOperationBuy = True

    ''' Попытка торговать '''
    def attemptToMakeTrade(self):
        # currentPrice = self.getMarketPrice()
        # percentageDiff = (currentPrice - self.lastOpPrice) / self.lastOpPrice
        # if self.isNextOperationBuy:
        #     self.tryToBuy(percentageDiff)
        # else:
        #     self.tryToSell(percentageDiff)
        return

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

    ''' Создаем список всех акций по FIGI и TICKER: '''
    def create_figi_tickers_json_file(self, file='assets/figi.json'):

        ''' Функция - сборщик инструментов: '''
        def my_list_collection(instrument, list_of_instruments):
            my_list = list()
            new_row = dict()
            for row in list_of_instruments:
                new_row = {
                    "figi": row.figi,
                    "ticker": row.ticker,
                    "name": row.name,
                    "instrument": instrument,
                    "class_code": row.class_code,
                    "exchange": row.exchange,
                    "currency": row.currency,
                    "country_of_risk_name": row.country_of_risk_name,
                    "sector": row.sector if instrument in ['bond', 'etf', 'future', 'share'] else ''
                }
                ''' Сборка и Проверка содержания по одному инструменту: '''
                # print(new_row)
                my_list.append(new_row)
            # print(my_list)
            return my_list

        ''' Соединяем все инструменты в один список: '''
        list_of_all_types_of_instruments = list()
        # for instrum in ['share', 'currency', 'bond', 'etf', 'future']:
        for instrum in ['share', 'currency']:
            list_of_all_types_of_instruments.extend(my_list_collection(instrum, self.get_any_instrument(instrument=instrum)))

        ''' Устаревший способ: Загружаем все акции-share: '''
        # list_of_all_types_of_instruments = my_list_collection('shares', self.get_all_shares())
        # all_shares = self.get_all_shares()
        # all_shares = goby.get_all_shares()['figi', 'ticker']
        # print(all_shares)

        ''' Создаем pandas-файл '''
        data = self.createPandasData(list_of_all_types_of_instruments, columns=['figi', 'ticker', 'name', 'class_code', 'exchange', 'currency', 'country_of_risk_name', 'sector'])
        ''' Запись в JSON-файл'''
        self.writeJson(data, file=file)
        return

    ''' Создаем pandas-файл '''
    def createPandasData(self, my_list, columns=["time", "high", "low", "open", "close", "volume", "is_complete"]):
        data = pd.DataFrame(list(my_list), columns=columns)
        # print(data)
        # data = data.set_index('time')
        # После вернуть формат: pd.to_datetime(1600355888, unit='s', origin='unix')
        # print('set_index - time: ')
        # Печатаем для проверки получившихся данных:
        # print("Данные data: ")
        # print(data.head(3))
        return data

    ''' Запись в JSON-файл'''
    def writeJson(self, data, file='assets/figi.json'):
        return data.to_json(file, orient="index", indent=2, force_ascii=False)

    ''' Чтение из JSON-файла'''
    def readJson(self, file='assets/figi.json'):
        data = pd.read_json(file, orient='index')
        # print("Данные из json-файла: ")
        # print(sj.head(3))
        return data

    ''' Получаем данные об акции из json-файла:'''
    def figi(self, ticker, file='assets/figi.json'):
        try:
            data = self.readJson(file=file)
            # print('data: ', data)
            # a = data.loc[data['ticker']==ticker,'figi']   # Возвращаем значение figi
            a = data.loc[data['ticker'] == ticker, 'figi'].iloc[0]   # Возвращаем значение figi
            return a
        except: return
    def ticker(self, figi, file='assets/figi.json'):
        try:
            data = self.readJson(file=file)
            # data.loc[data['figi']==figi]['ticker']   # Возвращаем значение ticker
            return data.loc[data['figi'] == figi, 'ticker'].iloc[0]   # Возвращаем значение ticker
        except: return
    def name(self, figi, file='assets/figi.json'):
        try:
            data = self.readJson(file=file)
            # data.loc[data['figi']==figi]['name']   # Возвращаем значение name
            return data.loc[data['figi'] == figi, 'name'].iloc[0]   # Возвращаем значение name
        except: return
    def class_code(self, ticker, file='assets/figi.json'):
        try:
            data = self.readJson(file=file)
            # data.loc[data['figi']==figi]['name']   # Возвращаем значение name
            return data.loc[data['ticker'] == ticker, 'class_code'].iloc[0]   # Возвращаем значение name
        except: return
    def exchange(self, figi, file='assets/figi.json'):
        try:
            data = self.readJson(file=file)
            # data.loc[data['figi']==figi]['exchange']   # Возвращаем значение exchange
            return data.loc[data['figi'] == figi, 'exchange'].iloc[0]   # Возвращаем значение name
        except: return
    def currency(self, figi, file='assets/figi.json'):
        try:
            data = self.readJson(file=file)
            # data.loc[data['figi']==figi]['currency']   # Возвращаем значение currency
            return data.loc[data['figi'] == figi, 'currency'].iloc[0]   # Возвращаем значение name
        except: return
    ''' Получаем подробные данные об акции из json-файла:'''
    def share_brief_info(self, figi:str = None, ticker:str = None, file='assets/figi.json'):
        data = self.readJson(file=file)
        if figi: return data.loc[data['figi']==figi]
        # elif ticker: return data.loc[data['ticker']==ticker].iloc[[0],[1]]
        # elif ticker: return data.loc[data['ticker']==ticker].iloc[0].iloc[0]
        elif ticker: return data.loc[data['ticker'] == ticker].iloc[0]
        else: return

    ''' Печать графика акции: '''
    def graphPltPrint(self, data):
        plt.title('График инструмента: ')
        plt.grid()
        plt.plot(data.loc['high'], label='high')
        plt.plot(data.loc['low'], label='low')
        plt.plot(data.loc['open'], label='open')
        plt.plot(data.loc['close'], label='close')
        plt.legend()
        plt.show()

    ''' Выводим график на экран '''
    def graphFinPrint(self, data, title='', type='candle', volume=True):
        # type='candle', type='bars, type='ohlc', type='line', type='renko' type='pnf'

        ''' Переводим формат даты из str в datetime: '''
        # data.index = pd.to_datetime(data.columns['time'])
        data['time'] = pd.to_datetime(data['time'], infer_datetime_format=True)
        # data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')

        ''' Переиндексация: колонка time -> в index "Date": '''
        data = data.set_index('time')

        ''' Смена названия столбца index по требованию библиотеки mpf'''
        # data.index.rename('Date')  # sj = sj.rename(index={'Date'} или # sj = sj.reindex(sj.index.rename('Date'))
        # print("Данные sj после переиндексации time -> Date: ")
        # print(sj.head())

        ''' Печать графика: '''
        # mpf.plot(data, type='candle')
        # mpf.plot(data, type='candle', mav=(3, 6, 9), volume=True, show_nontrading=True)
        mpf.plot(data, type=type, volume=volume, title=title)

    ''' Обработка ошибок '''
    def badRequestError(self):
        # print('Обнаружена ошибка: ', error)   # class 'tinkoff.invest.exceptions.RequestError':
        # print(error.code, error.details, error.metadata)
        return error

''' Тестирование методов класса Goby '''
# if __name__ == '__main__':

    # ''' Тестирование токена и переменных класса'''
    # stock = Goby("MXL")
    # print(stock.getToken())
    # print(stock.__dict__)
    # print(getattr(stock, '_Goby__tsc_token'))
    # setattr(stock, '_Goby__tsc_token', 'Tok')
    # print(getattr(stock, '_Goby__tsc_token'))


    # ''' Запрос содержания портфеля '''
    # goby = Goby()
    # print(client.getPortfolio())
    # print(client.getMarketBonds())
    # print(client.getMarketStocks())
    # print(client.getMarketByTicker(ticker='AAPL'))
    # [print(x) for x in client.getMarketByTicker(ticker='AAPL')]
    # pprint(client.getMarketByTicker(ticker='AAPL'))

    # a = goby.my_generator(3)
    # [print(b) for b in a]

    # ''' Проверка токена '''
    # print((client.getToken()))
    # ''' Проверка службы сервиса сандбокс'''
    # print(client.sandbox_service())

    # '''
    # УПРАЖНЕНИЯ С АККАУНТАМИ:
    # '''
    # ''' Список активных аккаунтов '''
    # acc = goby.get_snb_accounts()
    # print('Аккаунт (id): ', acc[0].id)
    # ''' Открываем аккаунты '''
    # acc1 = goby.open_snb_account()
    # print('Новый аккаунт: ', acc1)
    # ''' Закрываем аккаунты'''
    # goby.close_snb_account('8d6e2973-b8d5-4fdd-8e6e-0058f724ad12')
    # [print(x) for x in acc_2]

    # '''
    # УПРАЖНЕНИЯ С ИНСТРУМЕНТАМИ:
    # '''
    # ''' Список последних цен на все инструменты '''
    # all_prices = goby.get_last_prices()
    # print('quotation для инструмента: ', all_prices)

    # ''' Запрос инструмента: '''
    # ticker, figi = '',''
    # ticker: str = 'FNKO'
    # # figi: str = 'BBG000B9XRY4'   # AAPL
    #
    #
    # ''' Данные об акции '''
    # if ticker: share_info = goby.getInstrumentInfo(ticker=ticker)
    # else: share_info = goby.getInstrumentInfo(figi=figi)
    # print(f'Данные по акции: ticker: {share_info.ticker}, figi: {share_info.figi}, name: {share_info.name}, sector: {share_info.sector}, country: {share_info.country_of_risk_name} ')
    #
    # '''Последняя цена на инструмент: '''
    # # print('share_info.figi: ', type(share_info.figi), share_info.figi)
    # price = goby.get_last_price(figi=str(share_info.figi))
    # # print(f'Последняя цена на {share_info.ticker}: {price[0].price}')
    # print(f'Последняя цена на {share_info.ticker}: {goby.price_to_float(price[0].price)}, '
    #       f'время сделки: {goby.utc_2_msc(price[0].time)}')
    #
    # ''' Запрос исторических свечей '''
    # from_ = datetime.datetime(2022, 1, 1)
    # to = datetime.datetime.now()
    # interval = 5
    # '''
    #         Name:                           Number: Description:
    #         CANDLE_INTERVAL_UNSPECIFIED     0       Интервал не определён.
    #         CANDLE_INTERVAL_1_MIN           1       1 минута.
    #         CANDLE_INTERVAL_5_MIN           2       5 минут.
    #         CANDLE_INTERVAL_15_MIN          3       15 минут.
    #         CANDLE_INTERVAL_HOUR            4       1 час.
    #         CANDLE_INTERVAL_DAY             5       1 день.
    # '''
    # # request = dict(figi=figi, from_=from_, to=to, interval=interval)
    # # print(request)
    # share_candle = goby.get_stock_candles(share_info.figi, from_, to, interval)
    # # print(stock_candle)
    #
    # ''' Создаем List-файл '''
    # my_list = goby.createListData(share_candle)
    # ''' Создаем pandas-файл '''
    # data = goby.createPandasData(my_list)
    #
    # ''' Запись в JSON-файл'''
    # data = goby.writeJson(data, file='stock.json')
    # ''' Чтение из JSON-файла'''
    # data = goby.readJson(file='stock.json')
    #
    # ''' Выводим график инструмента на экран '''
    # goby.graphFinPrint(data, title=share_info.name, type='candle')