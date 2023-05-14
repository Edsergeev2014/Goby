from decouple import AutoConfig
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest.clients import Client

from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
from tinkoff.invest.constants import INVEST_GRPC_API
# INVEST_GRPC_API - "боевой",
# INVEST_GRPC_API_SANDBOX - "песочница"

''' OnlyRead Token'''
__config = AutoConfig(search_path='assets/tsc_tokens/onlyread')
''' Sandbox Token'''
# __config = AutoConfig(search_path='assets/tsc_tokens/sandbox')

__tsc_token = __config('TSC_TOKEN')
# print(__tsc_token)

print("SandboxClient: ")
with SandboxClient(token=__tsc_token) as client:
    print(client.sandbox.get_sandbox_accounts())

# with Client(token=__tsc_token, target=INVEST_GRPC_API_SANDBOX) as client:
    # print(client.users.get_accounts())
    # print(client.users.get_info())
    # pass

# from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX
# Переключение между контурами реализовано через target,
# INVEST_GRPC_API - "боевой",
# INVEST_GRPC_API_SANDBOX - "песочница"

print("Client: ")
with Client(token=__tsc_token, target=INVEST_GRPC_API_SANDBOX) as client:
# with Client(token=__tsc_token, target=INVEST_GRPC_API) as client:
        print(client.users.get_accounts())
        print(client.users.get_info())
#     print(client.users.get_info())

# with Client(__tsc_token, target=INVEST_GRPC_API_SANDBOX) as client:
# with Client(__tsc_token, target=INVEST_GRPC_API) as client:
    # x = client.instruments.shares().instruments
    # print(x)
    # pass