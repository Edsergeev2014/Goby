from decouple import AutoConfig
from tinkoff.invest.sandbox.client import Client
from tinkoff.invest.services import SandboxService as sandboxclient

__config = AutoConfig(search_path='assets/tsc_tokens/sandbox')
__tsc_token = __config('TSC_TOKEN')
# __tsc_token = 't.BEKlBzkKpyoQMaXEh9a3GNoPPU0WqY0eSQsippnNwWN0C9GnKIt-_qg7Y1k0nEs_T5OiuMaK4UfuOw20C4pTQQ'
# print(__tsc_token)

with Client(__tsc_token) as client:
    # print(client.users.get_info())
    ''' АККАУНТЫ '''
    accounts = client.sandbox.get_sandbox_accounts()
    # new_account = client.sandbox.open_sandbox_account()
    print("Аккаунты: ", accounts)
    ''' ПОРТФОЛИО '''
    # print("Портфолио: ", client.sandbox.get_sandbox_portfolio(account_id=accounts[0]))
    # print(SandboxService.get_sandbox_accounts())
    # print(client.users.get_accounts())
    if accounts is not None:
        # ''' Печать Развернутого содержания счета '''
        print('Счета: ')
        response = client.sandbox.get_sandbox_accounts()
        for account in response.accounts:
            print('=> ', account.id, 'Название счёта:', account.name, 'Статус:', account.status,
                  account.type, sep='\n')
            print("Портфель: ", client.sandbox.get_sandbox_portfolio(account_id=account.id))