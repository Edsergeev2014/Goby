from tinkoff.invest import OperationType, OrderExecutionReportStatus, OrderDirection, AccountStatus
from tinkoff.invest import TradingSchedule, SecurityTradingStatus

class Description():


    ''' Обработка инструментов '''
    def currency_type(self, currency_type: str = None, flag: str = None, capitalize: bool = False):
        # flag: key-раздел, value-значение, val-значение, simbol-символы, None-пока ничего
        if flag == 'key':
            if currency_type.lower() == 'rub': currency_type_rus = 'рубли'
            elif currency_type.lower() == 'usd': currency_type_rus = 'доллары'
            elif currency_type.lower() == 'eur': currency_type_rus = 'евро'
            else: currency_type_rus = 'неопределено'
        elif flag == 'value':
            if currency_type.lower() == 'rub': currency_type_rus = 'рублей'
            elif currency_type.lower() == 'usd': currency_type_rus = 'долларов'
            elif currency_type.lower() == 'eur': currency_type_rus = 'евро'
            else: currency_type_rus = 'неопределено'
        elif flag == 'val':
            if currency_type.lower() == 'rub': currency_type_rus = 'руб.'
            elif currency_type.lower() == 'usd': currency_type_rus = 'дол.'
            elif currency_type.lower() == 'eur': currency_type_rus = 'евро'
            else: currency_type_rus = 'неопределено'
        elif flag == 'simbol':
            if currency_type.lower() == 'rub': currency_type_rus = '₽'
            elif currency_type.lower() == 'usd': currency_type_rus = '$'
            elif currency_type.lower() == 'eur': currency_type_rus = '€'
            else: currency_type_rus = ' '
        else:
            if currency_type.lower() == 'rub': currency_type_rus = 'рублей'
            elif currency_type.lower() == 'usd': currency_type_rus = 'долларов'
            elif currency_type.lower() == 'eur': currency_type_rus = 'евро'
            else: currency_type_rus = 'неопределено'


        if all([capitalize is True, currency_type_rus is not None]): return currency_type_rus.capitalize()
        else: return currency_type_rus


    ''' Обработка инструментов '''
    def instrument_type(self, instrument_type: str = None, capitalize: bool = False):
        if instrument_type == 'bond': instrument_type_rus = 'облигация'
        elif instrument_type == 'share': instrument_type_rus = 'акция'
        elif instrument_type == 'currency': instrument_type_rus = 'валюта'
        elif instrument_type == 'etf': instrument_type_rus = 'фонд'
        elif instrument_type == 'futures': instrument_type_rus = 'фьючерс'
        else: instrument_type_rus = None

        if all([capitalize is True, instrument_type_rus is not None]): return instrument_type_rus.capitalize()
        else: return instrument_type_rus

    ''' Обработка инструментов '''
    def operation_type_description(self, argument: str = None):
        argument_number = OperationType(argument)
        # OPERATION_TYPE_BUY = 15 => 'Покупка ЦБ'

        if argument_number == 0: argument_rus = 'Тип операции не определён'     # OPERATION_TYPE_UNSPECIFIED
        elif argument_number == 1: argument_rus = 'Завод денежных средств'      # OPERATION_TYPE_INPUT
        elif argument_number == 2: argument_rus = 'Удержание налога по купонам'     # OPERATION_TYPE_BOND_TAX
        elif argument_number == 3: argument_rus = 'Вывод ЦБ'        # OPERATION_TYPE_OUTPUT_SECURITIES
        elif argument_number == 4: argument_rus = 'Доход по сделке РЕПО овернайт'       # OPERATION_TYPE_OVERNIGHT
        elif argument_number == 5: argument_rus = 'Удержание налога'        # OPERATION_TYPE_TAX
        elif argument_number == 6: argument_rus = 'Полное погашение облигаций'      # OPERATION_TYPE_BOND_REPAYMENT_FULL
        elif argument_number == 7: argument_rus = 'Продажа ЦБ с карты'      # OPERATION_TYPE_SELL_CARD
        elif argument_number == 8: argument_rus = 'Удержание налога по дивидендам'      # OPERATION_TYPE_DIVIDEND_TAX
        elif argument_number == 9: argument_rus = 'Вывод денежных средств'      # OPERATION_TYPE_OUTPUT
        elif argument_number == 10: argument_rus = 'Частичное погашение облигаций'       # OPERATION_TYPE_BOND_REPAYMENT
        elif argument_number == 11: argument_rus = 'Корректировка налога'        # OPERATION_TYPE_TAX_CORRECTION
        elif argument_number == 12: argument_rus = 'Удержание комиссии за обслуживание брокерского счёта'        # OPERATION_TYPE_SERVICE_FEE
        elif argument_number == 13: argument_rus = 'Удержание налога за материальную выгоду'     # OPERATION_TYPE_BENEFIT_TAX
        elif argument_number == 14: argument_rus = 'Удержание комиссии за непокрытую позицию'        # OPERATION_TYPE_MARGIN_FEE
        elif argument_number == 15: argument_rus = 'Покупка:'      # OPERATION_TYPE_BUY
        elif argument_number == 16: argument_rus = 'Покупка ЦБ с карты'      # OPERATION_TYPE_BUY_CARD
        elif argument_number == 17: argument_rus = 'Завод ЦБ'        # OPERATION_TYPE_INPUT_SECURITIES
        elif argument_number == 18: argument_rus = 'Продажа в результате Margin-call'        # OPERATION_TYPE_SELL_MARGIN
        elif argument_number == 19: argument_rus = 'Удержание комиссии за операцию'      # OPERATION_TYPE_BROKER_FEE
        elif argument_number == 20: argument_rus = 'Покупка в результате Margin-call'        # OPERATION_TYPE_BUY_MARGIN
        elif argument_number == 21: argument_rus = 'Выплата дивидендов'      # OPERATION_TYPE_DIVIDEND
        elif argument_number == 22: argument_rus = 'Продажа:'      # OPERATION_TYPE_SELL
        elif argument_number == 23: argument_rus = 'Выплата купонов'     # OPERATION_TYPE_COUPON
        elif argument_number == 24: argument_rus = 'Удержание комиссии SuccessFee'       # OPERATION_TYPE_SUCCESS_FEE
        elif argument_number == 25: argument_rus = 'Передача дивидендного дохода'        # OPERATION_TYPE_DIVIDEND_TRANSFER
        elif argument_number == 26: argument_rus = 'Зачисление вариационной маржи'       # OPERATION_TYPE_ACCRUING_VARMARGIN
        elif argument_number == 27: argument_rus = 'Списание вариационной маржи'     # OPERATION_TYPE_WRITING_OFF_VARMARGIN
        elif argument_number == 28: argument_rus = 'Покупка в рамках экспирации фьючерсного контракта'       # OPERATION_TYPE_DELIVERY_BUY
        elif argument_number == 29: argument_rus = 'Продажа в рамках экспирации фьючерсного контракта'       # OPERATION_TYPE_DELIVERY_SELL
        elif argument_number == 30: argument_rus = 'Комиссия за управление по счёту автоследования'      # OPERATION_TYPE_TRACK_MFEE
        elif argument_number == 31: argument_rus = 'Комиссия за результат по счёту автоследования'       # OPERATION_TYPE_TRACK_PFEE
        elif argument_number == 32: argument_rus = 'Удержание налога по ставке 15%'      # OPERATION_TYPE_TAX_PROGRESSIVE
        elif argument_number == 33: argument_rus = 'Удержание налога по купонам по ставке 15%'       # OPERATION_TYPE_BOND_TAX_PROGRESSIVE
        elif argument_number == 34: argument_rus = 'Удержание налога по дивидендам по ставке 15%'        # OPERATION_TYPE_DIVIDEND_TAX_PROGRESSIVE
        elif argument_number == 35: argument_rus = 'Удержание налога за материальную выгоду по ставке 15%'       # OPERATION_TYPE_BENEFIT_TAX_PROGRESSIVE
        elif argument_number == 36: argument_rus = 'Корректировка налога по ставке 15%'      # OPERATION_TYPE_TAX_CORRECTION_PROGRESSIVE
        elif argument_number == 37: argument_rus = 'Удержание налога за возмещение по сделкам РЕПО по ставке 15%'        # OPERATION_TYPE_TAX_REPO_PROGRESSIVE
        elif argument_number == 38: argument_rus = 'Удержание налога за возмещение по сделкам РЕПО'      # OPERATION_TYPE_TAX_REPO
        elif argument_number == 39: argument_rus = 'Удержание налога по сделкам РЕПО'        # OPERATION_TYPE_TAX_REPO_HOLD
        elif argument_number == 40: argument_rus = 'Возврат налога по сделкам РЕПО'      # OPERATION_TYPE_TAX_REPO_REFUND
        elif argument_number == 41: argument_rus = 'Удержание налога по сделкам РЕПО по ставке 15%'      # OPERATION_TYPE_TAX_REPO_HOLD_PROGRESSIVE
        elif argument_number == 42: argument_rus = 'Возврат налога по сделкам РЕПО по ставке 15%'        # OPERATION_TYPE_TAX_REPO_REFUND_PROGRESSIVE
        elif argument_number == 43: argument_rus = 'Выплата дивидендов на карту'     # OPERATION_TYPE_DIV_EXT
        else: argument_rus = None
        return argument_rus

    def orders_execution_report_status(self, argument: str = None):
        argument_number = OrderExecutionReportStatus(argument)
        if argument_number == 0: argument_rus = None                        # EXECUTION_REPORT_STATUS_UNSPECIFIED
        elif argument_number == 1: argument_rus = 'Исполнена'             # EXECUTION_REPORT_STATUS_FILL
        elif argument_number == 2: argument_rus = 'Отклонена'             # EXECUTION_REPORT_STATUS_REJECTED
        elif argument_number == 3: argument_rus = 'Отменена пользователем'# EXECUTION_REPORT_STATUS_CANCELLED
        elif argument_number == 4: argument_rus = 'В обработке'           # EXECUTION_REPORT_STATUS_NEW
        elif argument_number == 5: argument_rus = 'Частично исполнена'    # EXECUTION_REPORT_STATUS_PARTIALLYFILL
        else: argument_rus = None
        return argument_rus

    def order_direction(self, argument: str = None):
        argument_number = OrderExecutionReportStatus(argument)
        if argument_number == 0: argument_rus = 'Значение не указано'       # ORDER_DIRECTION_UNSPECIFIED
        elif argument_number == 1: argument_rus = 'Покупка'                 # ORDER_DIRECTION_BUY
        elif argument_number == 2: argument_rus = 'Продажа'                 # ORDER_DIRECTION_SELL
        else: argument_rus = None
        return argument_rus

    def account_status(self, argument: str = None):
        argument_number = AccountStatus(argument)
        if argument_number == 0: argument_rus = 'Статус счёта не определён'       # ACCOUNT_STATUS_UNSPECIFIED
        elif argument_number == 1: argument_rus = 'Новый, в процессе открытия'    # ACCOUNT_STATUS_NEW
        elif argument_number == 2: argument_rus = 'Открытый и активный счёт'      # ACCOUNT_STATUS_OPEN
        elif argument_number == 3: argument_rus = 'Закрытый счёт'                 # ACCOUNT_STATUS_CLOSED
        else: argument_rus = None
        return argument_rus

    # def exchanges(self, argument: str = None):
    #     argument_info = TradingSchedule(argument)
    #     # print('argument_info: ', argument_info)
    #     # print('argument_info.exchange: ', argument_info.exchange)
    #     # TradingSchedule(exchange='MOEX', days=[TradingDay(date=datetime.datetime(2022, 3, 2, 0, 0, tzinfo=datetime.timezone.utc), is_trading_day=True, start_time=datetime.datetime(2022, 3, 2, 7, 0, tzinfo=datetime.timezone.utc), end_time=datetime.datetime(2022, 3, 2, 15, 39, tzinfo=datetime.timezone.utc), market_order_start_time=datetime.datetime(2022, 3, 2, 7, 0, tzinfo=datetime.timezone.utc), market_order_end_time=datetime.datetime(2022, 3, 2, 15, 45, tzinfo=datetime.timezone.utc))]),
    #     if argument_info.exchange == 'MOEX': argument_rus = ["Московская биржа","Торги на фондовом рынке с 09:50 до 18:50.", "Аукцион открытия: 09:50—10:00. Основная торговая сессия: 10:00—18:40. Аукцион закрытия: 18:40—18:50"]
    #     elif argument_info.exchange == 'MOEX_INVESTBOX': argument_rus = ["Московская биржа INVESTBOX","",""]
    #     elif argument_info.exchange == 'MOEX_MORNING': argument_rus = ["Московская биржа MORNING","",""]
    #     elif argument_info.exchange == 'MOEX_PLUS': argument_rus = ["Московская биржа PLUS", "Торги на фондовом рынке + вечерняя сессия.", "Аукцион открытия: 09:50 — 10:00. Основная торговая сессия: 10:00—18:40. Аукцион закрытия: 18:40—18:50. Аукцион открытия: 19:00—19:05. Вечерняя торговая сессия: 19:05—23:50"]
    #     elif argument_info.exchange == 'MOEX_EVENING_WEEKEND': argument_rus = ["Московская биржа","Торги на фондовом рынке + вечерняя сессия + торговля на выходных","Аукцион открытия: 09:50 — 10:00. Основная торговая сессия: 10:00—18:40. Аукцион закрытия: 18:40—18:50. Аукцион открытия: 19:00—19:05. Вечерняя торговая сессия: 19:05—23:50. Основная торговая сессия выходного дня: 10:00—19:00"]
    #     elif argument_info.exchange == 'SPB': argument_rus = ["СПБ Биржа","",""]
    #     elif argument_info.exchange == 'SPB_DE': argument_rus = ["СПБ Биржа DE","",""]
    #     elif argument_info.exchange == 'SPB_DE_MORNING': argument_rus = ["СПБ Биржа MORNING","",""]
    #     elif argument_info.exchange == 'SPB_EUROBONDS': argument_rus = ["СПБ Биржа EUROBONDS","",""]
    #     elif argument_info.exchange == 'SPB_MORNING': argument_rus = ["СПБ Биржа MORNING","",""]
    #     elif argument_info.exchange == 'SPB_MORNING_WEEKEND': argument_rus = ["СПБ Биржа MORNING_WEEKEND","",""]
    #     elif argument_info.exchange == 'SPB_RU_MORNING': argument_rus = ["СПБ Биржа RU_MORNING","",""]
    #     elif argument_info.exchange == 'SPB_WEEKEND': argument_rus = ["СПБ Биржа WEEKEND","",""]
    #     elif argument_info.exchange == 'NYSE': argument_rus = ["NYSE биржа","",""]
    #     else: return ['--', '--', '--']
    #     # print('argument_rus: ', argument_info.exchange, type(argument_rus), argument_rus)
    #     return argument_rus

    def exchange_activity(self, period: str = None, argument: bool = False):
        if period == 'day':
            return 'торговый день' if argument else 'неторговый день'
        elif period == 'time':
            return 'торговое время' if argument else 'неторговое время'
        elif period == 'status':
            return 'Биржа открыта' if argument else 'Биржа закрыта'
        else:
            return None

    def trading_status(self, argument: str = None):
        argument_text = SecurityTradingStatus(argument)
        if argument_text == 0: argument_number = 0
        elif argument_text == 1: argument_number = 1
        elif argument_text == 2: argument_number = 2
        elif argument_text == 3: argument_number = 3
        elif argument_text == 4: argument_number = 4
        elif argument_text == 5: argument_number = 5
        else: argument_number = None
        # else: argument_rus = None
        return argument_number
        # Расшифровка значений: https://tinkoff.github.io/investAPI/instruments/#instrumentstatus
