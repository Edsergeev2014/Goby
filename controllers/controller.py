from controllers.asyncloopthread import AsyncLoopThread
import asyncio

from models.info import Info

class Controller_Info():
    def __init__(self):
        self.info = Info()
        self.current_datetime = self.info.current_datetime

    async def exchanges_schedules(self):
        # await asyncio.sleep(1)
        # get = 'Test'
         return await self.info.exchanges_schedules()

    def exchanges_table_head(self):
        return self.info.exchanges_table_head()

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