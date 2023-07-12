''' Модель Info'''
from goby_test import Goby
from controllers.asyncloopthread import AsyncLoopThread
import asyncio
import time, datetime
from assets.color import color as cls
from assets.arguments import Description
from models.info_slave import InfoSlave

class Info():
    def __init__(self):
        self.goby = Goby()
        self.slave = InfoSlave()
        ''' Текущий день и время '''
        self.current_datetime = self.goby.get_msc(self.goby.current_datetime(),
                                                  is_datetime='datetime')

    ''' БИРЖИ И РАСПИСАНИЕ '''
    ''' Режим и расписание торгов на биржах '''
    def exchanges_table_head(self):
        response = list(['Биржа','Сегодня','Открытие сессии','Закрытие сессии'])
        return response

    ''' Получить расписание работы бирж из списка бирж '''
    async def get_exchanges_activity(self, content: str = None, exchanges: list = None, sorted: bool = False):
        # response = self.get_trading_activity()
        response = await self.goby.get_trading_activity()
        # print('Весь список бирж. get_trading_activity: ', response)
        # return response     # возвращает Весь список бирж
        description = Description()
        # trading_day = self.goby.trading_day()
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
                                                 # Выделенные биржи - основные в списке
                                                 exchange_en=exchange_info.exchange,
                                                 exchange_main = True if exchange_info.exchange in self.slave.exchanges_main() else False,
                                                 # Ближайший день в расписании биржи:
                                                 day=self.goby.get_msc(trading_days_info.date, is_datetime='date'),
                                                 # Является ли торговым днем:
                                                 is_trading_day=trading_days_info.is_trading_day,
                                                 # Проверка на торговый день:
                                                 exchange_day_activity_description=description.exchange_activity(period='day', argument=trading_days_info.is_trading_day),
                                                 # Время старта торгов:
                                                 start_time=self.slave.check_notime(self.goby.get_msc(trading_days_info.start_time, is_datetime='datetime')),
                                                 # Время окончания торгов:
                                                 end_time=self.slave.check_notime(self.goby.get_msc(trading_days_info.end_time, is_datetime='datetime')),
                                                 # market_order_start_time=self.get_msc(trading_days_info.market_order_start_time, is_datetime='time'),
                                                 # market_order_end_time=self.get_msc(trading_days_info.market_order_end_time, is_datetime='time'),
                                                 today='Сегодня' if self.goby.get_msc(trading_days_info.date, is_datetime='date') == self.goby.get_msc(datetime.datetime.now(), is_datetime='date') else self.goby.get_msc(trading_days_info.date, is_datetime='date'),
                                                 # Проверка на торговое время:
                                                 exchange_time_activity_description=description.exchange_activity(period='time', argument=self.exchange_time_activity(start_time=trading_days_info.start_time, end_time=trading_days_info.end_time)),
                                                 # Проверка на торговый день и торговое время биржи:
                                                 exchange_activity_status=True if trading_days_info.is_trading_day and self.exchange_time_activity(start_time=trading_days_info.start_time, end_time=trading_days_info.end_time) else False,
                                                 exchange_activity_status_description=description.exchange_activity(period='status', argument=True) if trading_days_info.is_trading_day and self.exchange_time_activity(start_time=trading_days_info.start_time, end_time=trading_days_info.end_time) else description.exchange_activity(period='status', argument=False)
                                                 )
                            # print('exchange_info: ', exchange_info)
                            # print('exchange_data: ', exchange_data)
                            response_list.append(exchange_data)
                    # Сортируем список бирж по названию, если задано это условие:
                    if sorted:
                        # Определяем ключ для сортировки (название биржи):
                        def target_key(target_exchanges):
                            return target_exchanges['exchange']
                        # print("response_list: ", type(response_list), response_list)
                        response_list.sort(key=target_key)
                # print('response_list: ', response_list)
                return response_list
        else:
            return response

    ''' Список бирж '''
    async def exchanges_schedules(self):
        response = await self.get_exchanges_activity(content='list_dict',
                                                          exchanges=['MOEX',
                                                                     'MOEX_INVESTBOX',
                                                                     'MOEX_MORNING',
                                                                     'MOEX_PLUS',
                                                                     'SPB',
                                                                     'SPB_DE',
                                                                     'SPB_DE_MORNING',
                                                                     'SPB_EUROBONDS',
                                                                     'SPB_MORNING',
                                                                     'SPB_MORNING_WEEKEND',
                                                                     'SPB_RU_MORNING',
                                                                     'SPB_WEEKEND',
                                                                     'NYSE'
                                                                     ],
                                                          sorted=True)
        # exchanges_main = self.slave.exchanges_main()
        # for schedule in exchanges_schedules
        # print(response)
        return response

    ''' Название бирж на русском язые '''
    def exchange_ru(self, exchange: str=None):
        description = Description()
        return description.exchanges(exchange)

    ''' Проверка активности (открытости) биржи'''
    def exchange_time_activity(self, start_time, end_time, *current_datetime ):

        # Приводим время к единому формату для последующего сравнения:
        start_time = self.goby.standart_date_time(self.goby.get_msc(start_time, is_datetime='datetimesec'), is_datetime='datetimesec')
        end_time = self.goby.standart_date_time(self.goby.get_msc(end_time, is_datetime='datetimesec'), is_datetime='datetimesec')

        # Проверяем, не пустое ли значение текущего времени:
        # print('current_datetime: ', type(current_datetime), current_datetime)
        if not current_datetime:
            current_datetime = self.goby.current_datetime()
        # current_datetime_utc =self.goby.current_datetime()-datetime.timedelta(hours=3)
        current_datetime = self.goby.get_msc(current_datetime, is_datetime='datetimesec')
        current_datetime = self.goby.standart_date_time(current_datetime, is_datetime='datetimesec')

        # Проверяем данные:
        # print('current_datetime: ', type(current_datetime), current_datetime)
        # print('start_time: ', type(start_time), start_time)
        # print('end_time: ', type(end_time), end_time)
        # print('True' if start_time <= current_datetime <= end_time else 'False')
        # print()

        # Сравниваем, находится ли текущее время в диапазоне start и end:
        if start_time <= current_datetime <= end_time:
            return True
        else:
            return False

    ''' Получить расписание биржи на предстоящий период '''
    # async def exchange_schedule(self, exchange):
    #     response = await self.goby.get_trading_schedules()
    #     print(response)
    #     return response

    ''' Заголовки столбцов для расписания биржи '''
    def get_exchange_schedule_per_week_table_head(self):
        response = list(['Дата','Статус','Открытие','Закрытие', 'Открытие премаркета','Закрытие премаркета'])
        return response

    # Запрос на расписание биржи на предстоящую неделю:
    async def get_exchange_schedule_per_week(self, exchange: str = None):
        # response = self.get_trading_activity()
        response = await self.goby.get_trading_schedules(exchange=exchange)
        # print('get_exchange_schedule_per_week: ', type(response), response)
        # return response     # возвращает Весь список бирж
        description = Description()
        # trading_day = self.goby.trading_day
        # Если ответ на запрос о расписании биржи не пустой:
        if response.exchange is not None:
            # Заготавливаем список для расписания по предстоящим дням
            response_list = list()
            # print('response: ', response)
            # Выполняем: Цикл по списку будущих дат работы биржи,
            # формируем для биржи: exchange_info.exchange, exchange_info.days
            # далее: цикл по exchange_info.days - TradingDay каждой биржи.
            # Получаем график работы биржи:
            # exchange_info cостоит из: exchange_info.exchange, exchange_info.days
            exchange = description.exchanges(response.exchange)
            days_info = response.days
            for trading_days_info in days_info:
                exchange_data = dict(day=self.goby.get_msc(trading_days_info.date, is_datetime='date'),
                                     # Является ли торговым днем:
                                     is_trading_day=trading_days_info.is_trading_day,
                                     # Проверка на торговый день:
                                     exchange_activity_status_description=description.exchange_activity(period='status', argument=trading_days_info.is_trading_day),
                                     exchange_day_activity_description=description.exchange_activity(period='day', argument=trading_days_info.is_trading_day),
                                     # Время старта торгов:
                                     start_time=self.slave.check_notime(self.goby.get_msc(trading_days_info.start_time, is_datetime='datetime')),
                                     # Время окончания торгов:
                                     end_time=self.slave.check_notime(self.goby.get_msc(trading_days_info.end_time, is_datetime='datetime')),
                                     # market_order_start_time=self.get_msc(trading_days_info.market_order_start_time, is_datetime='time'),
                                     # market_order_end_time=self.get_msc(trading_days_info.market_order_end_time, is_datetime='time'),
                                     # premarket_start_time=self.slave.check_notime(self.goby.get_msc(trading_days_info.premarket_start_time, is_datetime='datetime')),
                                     # premarket_end_time=self.slave.check_notime(self.goby.get_msc(trading_days_info.premarket_end_time, is_datetime='datetime'))
                                     )
                # print('exchange_info: ', exchange_info)
                # print('exchange_data: ', exchange_data)
                response_list.append(exchange_data)
            # print('response_list: ', response_list)
            return response_list
        else:
            return


    ''' АККАУНТЫ '''
    ''' Получить список открытых аккаунтов '''
    async def accounts(self, content: str = None):
        response = await self.goby.get_accounts()
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
                                        account_is_active=True if description.account_status(account.status) == description.account_status(2) else False,
                                        type=account.type)
                    # print('account: ', account)
                    # print('account_info: ', account_info)
                    response_list.append(account_info)
                # print('response_list: ', response_list)
                return response_list
        else:
            return response
        return
