from controllers.asyncloopthread import AsyncLoopThread
import asyncio

from models.info import Info
from models.instruments import T_Instruments
from models.portfolio import T_Portfolio

class Controller_Info():
    def __init__(self):
        self.info = Info()
        self.current_datetime = self.info.current_datetime

    async def exchanges_schedules(self):
        # await asyncio.sleep(1)
        # get = 'Test'
        return await self.info.exchanges_schedules()

    async def get_exchange_schedule_per_week(self, exchange: str = None):
        return await self.info.get_exchange_schedule_per_week(exchange)

    def exchanges_table_head(self):
        return self.info.exchanges_table_head()

    def exchange_ru(self,exchange):
        return self.info.exchange_ru(exchange)

    def get_exchange_schedule_per_week_table_head(self):
        return self.info.get_exchange_schedule_per_week_table_head()

    async def accounts(self):
        # return await self.info.accounts(content='list_dict')
        return await self.info.accounts(content='list_dict')

    async def coroutine_thread_1(self):
        # await asyncio.sleep(1)
        # get_2 = await self.info.get_trading_activity()
        # get_2 = 'Test'
        # print("Ответ от thread_2: ", get_2)
        return await self.exchanges_schedules()

    # Можно запустить через потоки, дополнительно к ассинхронности:
    async def run(self):
        thread_1 = AsyncLoopThread()
        thread_1.start()
        asyncio.run_coroutine_threadsafe(self.coroutine_thread_1(), thread_1.loop)
        return

class Controller_Instruments():
    def __init__(self):
        self.t_instruments = T_Instruments()

    # async def get_instruments_info_test(self):
    #     print('test')
    #     return "test"

    async def get_instruments_info(self, tickers: list = None, figies: list = None):
        # print('test')
        # return "test"
        if figies:
            # response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id='BBG000B9XRY4')
            response = await self.t_instruments.get_instruments_info(figies=figies)
        elif tickers:
            # response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER, class_code='SPBXM', id='AAPL')
            response = await self.t_instruments.get_instruments_info(tickers=tickers)
        # print("response: ", response)
        else:
            print("Control: Заполните данные по запросу акции")
            return None
        return response

class Controller_Portfolio():
    def __init__(self):
        self.t_portfolio = T_Portfolio()

    async def get_portfolio_positions(self):
        portfolio_positions = await self.t_portfolio.get_portfolio_positions()
        return portfolio_positions