import asyncio
from tinkoff.invest import (
    AsyncClient,
    CandleInstrument,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
)
from decouple import AutoConfig
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest.clients import Client

from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
from tinkoff.invest.constants import INVEST_GRPC_API
# INVEST_GRPC_API - "боевой",
# INVEST_GRPC_API_SANDBOX - "песочница"

''' OnlyRead Token'''
__config = AutoConfig(search_path='../assets/tsc_tokens/onlyread')
''' Sandbox Token'''
# __config = AutoConfig(search_path='assets/tsc_tokens/sandbox')

__tsc_token = __config('TSC_TOKEN')
# print(__tsc_token)

# print("SandboxClient: ")
# with SandboxClient(token=__tsc_token) as client:
#     print(client.sandbox.get_sandbox_accounts())

class AsyncoStream:
    def __init__(self, __tsc_token):
        self.__tsc_token = __tsc_token
    async def __call__(self, *args, **kwargs):
        with Client(token=self.__tsc_token) as client:
            yield client

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


    async for marketdata in __call__().market_data_stream.market_data_stream(
        request_iterator()
    ):
        print(marketdata)


responce = AsyncoStream(__tsc_token)
print(responce)