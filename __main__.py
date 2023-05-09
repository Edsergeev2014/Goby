from goby import Goby
import time
import datetime
import logging

''' Запуск основной программы '''
if __name__ == '__main__':
    print('Запуск программы... (проверка тайминга)')
    goby = Goby()
    try:
        ''' Статус торговой активности: '''
        trading_status = goby.get_trading_activity()
        # TradingSchedule(exchange='SPB', days=[
        #     TradingDay(date=datetime.datetime(2022, 2, 21, 0, 0, tzinfo=datetime.timezone.utc), is_trading_day=False,
        #                start_time=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        #                end_time=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        #                market_order_start_time=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
        #                market_order_end_time=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=datetime.timezone.utc))])
        # print('trading_status: ', type(trading_status), *trading_status)
        [print(item.days) for item in trading_status if item.exchange == 'MOEX']

        ''' Список активных аккаунтов '''
        accounts = goby.get_snb_accounts()
        account_id = accounts[0].id
        print('Аккаунт (id): ', account_id, '\n')

        ''' Содержание портфеля '''
        portfolio = goby.get_portfolio(account_id)
        print('Содержание портфеля: ', portfolio, '\n')
        print('Позиции в портфеле: ', *portfolio.positions, '\n')
        # print('Детализация total_amount_shares: ', type(portfolio.total_amount_shares), '\n')

        ''' Баланс портфеля '''
        balance_in_currencies = goby.get_balance(account_id)
        print('Баланс портфеля: ', balance_in_currencies, '\n')   # {'rub': 0.0, 'usd': 0, 'eur': 0}
        # print('Часть портфеля в USD: ', balance_in_currencies['usd'])

        ''' Выбор инструмента: '''
        ticker, figi = str(), str()
        ticker: str = 'AAPL'
        # figi: str = 'BBG000B9XRY4'   # AAPL

        ''' Данные по акции (подбор figi по ticker) '''
        share_info = goby.get_instrument_info(figi=figi, ticker=ticker)
        print(f'Данные по акции: ticker: {share_info.ticker}, figi: {share_info.figi}, name: {share_info.name}, sector: {share_info.sector}, country: {share_info.country_of_risk_name} ')

        ''' Цена инструмента (по последней сделке) '''
        price = goby.get_market_price(figi=share_info.figi)
        # print('price[0].price: ', type(price[0].price), price[0].price)
        print(f'Последняя цена на {share_info.ticker}: {goby.price_to_float(price[0].price)}, '
              f'время сделки: {goby.utc_2_msc(price[0].time)}')


        ''' Назначаем цену для ордера: '''
        ''' по последней сделке:'''
        price_order = goby.price_to_quotation(goby.price_to_float(price[0].price))
        '''по фиксированной цене: '''
        # price_order = goby.price_to_quotation(160.00)
        # price_order = goby.price_to_quotation(goby.price_float(price[0].price)) # Цену устанавливаем по последней сделке на рынке (текущую)
        # print('price_order: ', price_order, '\n')

        # ''' Пополняем счёт: '''
        # money = 200
        # currency = 'usd'
        # # amount_with_currency = goby.money_to_quotation(money=amount, currency=currency)
        # # print(f'Конвертация {amount} {currency}: ', amount_with_currency)
        # ''' Пополнение: '''
        # pay_in_response = goby.top_up_account(account_id=account_id, money=money, currency=currency)
        # '''Обновляем содержание портфеля: '''
        # if pay_in_response:
        #     print("Пополнен баланс портфеля.")
        #     balance_in_currencies = pay_in_response.balance
        #     # balance_in_currencies = goby.get_balance(account_id)
        #     print('Новый баланс портфеля: ', goby.money_value_float(balance_in_currencies), '\n')  # {'rub': 0.0, 'usd': 0, 'eur': 0}

        ''' Размещаем заявку-ордер: '''
        # Сделать обработку ошибки Internal 70001
        ''' Разместить ордер на покупку или продажу: '''
        # direction = 'BUY'   # 'SELL'
        # order_response = goby.place_order(figi=figi, quantity=1, price=price_order, direction=direction,
        #                                  account_id=account_id, order_type= "LIMIT", order_id="BUY317")
        # print('order_response: ', order_response, '\n')

        # Другие варианты:
        # order_response = goby.place_my_order(goby.order(account_id)) # Тестовый вариант
        # order_id = '40e6c3bc-4164-468a-aa9a-6769cf64bc28'

        ''' Отменяем заявку-ордер: '''
        # order_cancel = goby.order_cancel(request=goby.order(account_id=account_id, order_id='807c6be9-7d2b-408f-94d2-2d7644007ed2'), content='print')


        ''' Проверка активных заявок-ордеров: '''
        orders = goby.get_orders(request=goby.request_blank(account_id), content='print')
        # print('orders: ', orders, '\n')
        # print('orders: ', orders['order_id'])

        # order_cancel = goby.order_cancel(account_id=accounts[0].id, order_id=order_id)

        ''' Позиции в портфеле: '''
        portfolio_positions = goby.get_portfolio_positions(request=goby.request_blank(account_id), content='print')

        ''' Позиции: '''
        # positions = goby.get_positions(request=goby.request_blank(account_id))
        # print('positions: ', *positions.securities, '\n')

        ''' Список операций в портфеле за выбранный период: '''
        # print('goby.request_blank: ', goby.request_blank(account_id=account_id), '\n')
        operations = goby.get_operations(request=goby.request_blank(account_id=account_id), content='print')
        # print('operations: ', operations.operations, '\n')
        # print('operations: ', *operations.operations, '\n')


        ''' Создаем список всех акций по FIGI и TICKER: '''
        goby.create_figi_tickers_json_file(file='assets/figi.json')

        ''' Подстановка tiker вместо figi: '''
        print('AAPL => figi:', goby.figi('AAPL'))
        # print('AAPL: figi=', goby.figi(ticker='AAPL'))
        print('BBG000B9XRY4 => ticker:', goby.ticker('BBG000B9XRY4'))
        print('Информация по AAPL: \n', goby.share_brief_info(ticker='AAPL'))



    # ''' Обработка ошибок '''
    except goby.badRequestError() as error:
        print('Обнаружена ошибка:', error)  # error.code, error.details, error.metadata

    ''' 
    ГЛАВНЫЙ ЦИКЛ:
    '''
    # stock = Goby("MXL")
    # while True:
    #     goby.attemptToMakeTrade()
    #     time.sleep(5)       # Пауза - 30 сек.



