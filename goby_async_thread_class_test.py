import asyncio
from threading import Thread
from tinkoff.invest import (
    AsyncClient,
    CandleInstrument,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
)
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
# from tinkoff.invest.constants import INVEST_GRPC_API # !!! Боевой режим
# INVEST_GRPC_API - "боевой режим",
# INVEST_GRPC_API_SANDBOX - "песочница"

from decouple import AutoConfig
import time, datetime

# Режимы токенов:
''' OnlyRead Token'''
__config = AutoConfig(search_path='assets/tsc_tokens/onlyread')
''' Sandbox Token'''
# __config = AutoConfig(search_path='assets/tsc_tokens/sandbox')

__tsc_token = __config('TSC_TOKEN')
# print(__tsc_token)

class AsyncLoopThread(Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.loop = asyncio.new_event_loop()
    def run(self) -> None:
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

class Goby():
    def __init__(self):
        self.__config = AutoConfig(search_path='assets/tsc_tokens/onlyread')
        self.__tsc_token = self.__config('TSC_TOKEN')
        self.__target = INVEST_GRPC_API_SANDBOX

        '''Этот вариант не работает:
        # self.__async_client = AsyncClient(token=self.__tsc_token, target=self.__target)
        # функция:
        # async def action(self):
        #     action = AsyncClient(token=self.__tsc_token, target=self.__target)
        #     return action
        # и далее запрос:
        # async with self.__async_client as client:
        # ...   
        '''

    async  def get_accounts(self):
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
        # async with self.action() as client:
            accounts = await client.users.get_accounts()
        return accounts.accounts[0]
        # async with self.__async_client as client:
        #     await asyncio.sleep(1)
        #     response = client.users.get_accounts()
        #     print('client: ', client)
        #     print('accounts: ', client.users.get_accounts())
        #     # response = await self.test()
        #     # response = 'Probe'
        #     # print( "Открытые счета: ", response)
        #     return response.accounts
        #     # return client

    async def get_trading_schedules(self):
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
            response = await client.instruments.trading_schedules(from_=datetime.datetime.now(),to=datetime.datetime.now())
        return response.exchanges

    ''' Получить последнюю цену инструмента '''
    async def get_last_prices(self):
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
            response = await client.market_data.get_last_prices()
            # print("response: ", response)
        return response.last_prices

    async def get_last_price(self, figi=''):
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
            # response = client.market_data.get_last_prices(figi=figi)
            response = await client.market_data.get_last_prices(figi=[str(figi)])
            # print("response: ", response)
            return response.last_prices

    async def request_iterator(self):
        yield MarketDataRequest(
            subscribe_candles_request=SubscribeCandlesRequest(
                subscription_action=SubscriptionAction.SUBSCRIPTION_ACTION_SUBSCRIBE,
                instruments=[
                    CandleInstrument(
                        figi="BBG004730N88",
                        interval=SubscriptionInterval.SUBSCRIPTION_INTERVAL_ONE_MINUTE,
                    )
                ],
            )
        )
        while True:
            await asyncio.sleep(1)

    async def get_trading_activity(self):
        # await asyncio.sleep(1)
        # async with self.__async_client as client:
        async with AsyncClient(token=self.__tsc_token, target=self.__target) as client:
            async for marketdata in client.market_data_stream.market_data_stream(
                    self.request_iterator()
            ):
                print("Активность трейдинга: ", marketdata)

if __name__ == "__main__":
    goby = Goby()
    # loop = asyncio.get_event_loop()

    async def coroutine_thread_1():
        await asyncio.sleep(1)
        # get = 'Test'
        get_1 = await goby.get_accounts()
        print("Ответ от thread_1 (get_accounts): ", get_1)
        get_2 = await goby.get_trading_schedules()
        print("Ответ от thread_1 (get_trading_schedules): ", get_2)

        get_3 = await goby.get_last_price(figi='BBG005Q22HG8')
        print("Ответ от thread_1 (get_last_prices): ", get_3)

        return

    async def coroutine_thread_2():
        await asyncio.sleep(1)
        get_2 = await goby.get_trading_activity()
        # get_2 = 'Test'
        print("Ответ от thread_2: ", get_2)
        return

    thread_1 = AsyncLoopThread()
    thread_2 = AsyncLoopThread()

    thread_1.start()
    # print("Открытые счета: ", loop.run_until_complete(goby.get_accounts()))
    # print("Открытые счета: ", asyncio.run_coroutine_threadsafe(goby.get_accounts(), thread_1.loop))
    # status_1 = asyncio.run_coroutine_threadsafe(coroutine_thread_1(), thread_1.loop)
    # print("Статус ответа thread_1: ",status_1 )
    asyncio.run_coroutine_threadsafe(coroutine_thread_1(), thread_1.loop)
    time.sleep(3)

    # thread_2.start()
    # loop.run_until_complete(goby.get_trading_activity())
    # print("Активность трейдинга: ", goby.get_trading_activity())
    # print("Активность трейдинга: ", asyncio.run_coroutine_threadsafe(goby.get_trading_activity(), thread_2.loop))
    # asyncio.run_coroutine_threadsafe(coroutine_thread_2(), thread_2.loop)
    asyncio.run_coroutine_threadsafe(coroutine_thread_2(), thread_1.loop)
    time.sleep(3)

    # asyncio.run(goby.get_trading_activity())

