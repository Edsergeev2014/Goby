''' Модель Systems '''
# from goby_test import Goby
# from tinkoff.invest import RequestError as error
# import asyncio

# import pandas
import pandas as pd
# import matplotlib.pyplot as plt
# import mplfinance as mpf

class TinSystems():
    # def __init__(self):
    #     self.test = None
    #     # self.goby = Goby()
    #     # self.figi_tickers_json_file = 'assets/figi.json'
    #     # self.figi_tickers_json_file_test = 'assets/figi_test.json'

    # ''' Создаем список всех акций по FIGI и TICKER: '''
    # async def create_figi_tickers_json_file(self, file: str = None):
    #     file = self.figi_tickers_json_file
    #
    #     ''' Функция - сборщик инструментов: '''
    #     def my_list_collection(instrument, list_of_instruments):
    #         my_list = list()
    #         new_row = dict()
    #         for row in list_of_instruments:
    #             new_row = {
    #                 "figi": row.figi,
    #                 "ticker": row.ticker,
    #                 "name": row.name,
    #                 "instrument": instrument,
    #                 "class_code": row.class_code,
    #                 "exchange": row.exchange,
    #                 "currency": row.currency,
    #                 "country_of_risk_name": row.country_of_risk_name,
    #                 "sector": row.sector if instrument in ['bond', 'etf', 'future', 'share'] else ''
    #             }
    #             ''' Сборка и Проверка содержания по одному инструменту: '''
    #             # print(new_row)
    #             my_list.append(new_row)
    #         # print(my_list)
    #         return my_list
    #
    #     ''' Соединяем все инструменты в один список: '''
    #     list_of_all_types_of_instruments = list()
    #     # for instrum in ['share', 'currency', 'bond', 'etf', 'future']:
    #     for instrum in ['share', 'currency']:
    #         list_of_all_types_of_instruments.extend(my_list_collection(instrum, await self.goby.get_any_instrument(instrument=instrum)))
    #
    #     ''' Устаревший способ: Загружаем все акции-share: '''
    #     # list_of_all_types_of_instruments = my_list_collection('shares', self.get_all_shares())
    #     # all_shares = self.get_all_shares()
    #     # all_shares = goby.get_all_shares()['figi', 'ticker']
    #     # print(all_shares)
    #
    #     ''' Создаем pandas-файл '''
    #     data = self.createPandasData(list_of_all_types_of_instruments, columns=['figi', 'ticker', 'name', 'class_code', 'exchange', 'currency', 'country_of_risk_name', 'sector'])
    #     ''' Запись в JSON-файл'''
    #     self.writeJson(data, file=file)
    #     return
    #
    # ''' Создаем pandas-файл '''
    # def createPandasData(self, my_list, columns=["time", "high", "low", "open", "close", "volume", "is_complete"]):
    #     data = pd.DataFrame(list(my_list), columns=columns)
    #     # print(data)
    #     # data = data.set_index('time')
    #     # После вернуть формат: pd.to_datetime(1600355888, unit='s', origin='unix')
    #     # print('set_index - time: ')
    #     # Печатаем для проверки получившихся данных:
    #     # print("Данные data: ")
    #     # print(data.head(3))
    #     return data
    #
    # ''' Запись в JSON-файл'''
    # def writeJson(self, data, file: str = None):
    #     file = self.figi_tickers_json_file
    #     return data.to_json(file, orient="index", indent=2, force_ascii=False)

    ''' Чтение из JSON-файла'''
    def readJson(self, file: str = None):
        # file = self.figi_tickers_json_file
        file = '../assets/figi.json'
        data = pd.read_json(path_or_buf='../assets/figi.json', orient='index')
        # print("Данные из json-файла: ")
        # print(sj.head(3))
        return data

    # ''' Получаем данные об акции из json-файла:'''
    # def figi(self, ticker, file: str = None):
    #     file = self.figi_tickers_json_file
    #     try:
    #         data = self.readJson(file=file)
    #         # print('data: ', data)
    #         # a = data.loc[data['ticker']==ticker,'figi']   # Возвращаем значение figi
    #         a = data.loc[data['ticker'] == ticker, 'figi'].iloc[0]   # Возвращаем значение figi
    #         return a
    #     except: return
    # def ticker(self, figi, file: str = None):
    #     file = self.figi_tickers_json_file
    #     try:
    #         data = self.readJson(file=file)
    #         # data.loc[data['figi']==figi]['ticker']   # Возвращаем значение ticker
    #         return data.loc[data['figi'] == figi, 'ticker'].iloc[0]   # Возвращаем значение ticker
    #     except: return
    # def name(self, figi, file: str = None):
    #     file = self.figi_tickers_json_file
    #     try:
    #         data = self.readJson(file=file)
    #         # data.loc[data['figi']==figi]['name']   # Возвращаем значение name
    #         return data.loc[data['figi'] == figi, 'name'].iloc[0]   # Возвращаем значение name
    #     except: return
    # def class_code(self, ticker, file: str = None):
    #     file = self.figi_tickers_json_file
    #     try:
    #         data = self.readJson(file=file)
    #         # data.loc[data['figi']==figi]['name']   # Возвращаем значение name
    #         return data.loc[data['ticker'] == ticker, 'class_code'].iloc[0]   # Возвращаем значение name
    #     except: return
    # def exchange(self, figi, file: str = None):
    #     file = self.figi_tickers_json_file
    #     try:
    #         data = self.readJson(file=file)
    #         # data.loc[data['figi']==figi]['exchange']   # Возвращаем значение exchange
    #         return data.loc[data['figi'] == figi, 'exchange'].iloc[0]   # Возвращаем значение name
    #     except: return
    # def currency(self, figi, file: str = None):
    #     file = self.figi_tickers_json_file
    #     try:
    #         data = self.readJson(file=file)
    #         # data.loc[data['figi']==figi]['currency']   # Возвращаем значение currency
    #         return data.loc[data['figi'] == figi, 'currency'].iloc[0]   # Возвращаем значение name
    #     except: return
    # ''' Получаем подробные данные об акции из json-файла:'''
    # def share_brief_info(self, figi:str = None, ticker:str = None, file: str = None):
    #     file = self.figi_tickers_json_file
    #     data = self.readJson(file=file)
    #     if figi: return data.loc[data['figi']==figi]
    #     # elif ticker: return data.loc[data['ticker']==ticker].iloc[[0],[1]]
    #     # elif ticker: return data.loc[data['ticker']==ticker].iloc[0].iloc[0]
    #     elif ticker: return data.loc[data['ticker'] == ticker].iloc[0]
    #     else: return
    #
    # ''' Печать графика акции: '''
    # def graphPltPrint(self, data):
    #     plt.title('График инструмента: ')
    #     plt.grid()
    #     plt.plot(data.loc['high'], label='high')
    #     plt.plot(data.loc['low'], label='low')
    #     plt.plot(data.loc['open'], label='open')
    #     plt.plot(data.loc['close'], label='close')
    #     plt.legend()
    #     plt.show()
    #
    # ''' Выводим график на экран '''
    # def graphFinPrint(self, data, title='', type='candle', volume=True):
    #     # type='candle', type='bars, type='ohlc', type='line', type='renko' type='pnf'
    #
    #     ''' Переводим формат даты из str в datetime: '''
    #     # data.index = pd.to_datetime(data.columns['time'])
    #     data['time'] = pd.to_datetime(data['time'], infer_datetime_format=True)
    #     # data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')
    #
    #     ''' Переиндексация: колонка time -> в index "Date": '''
    #     data = data.set_index('time')
    #
    #     ''' Смена названия столбца index по требованию библиотеки mpf'''
    #     # data.index.rename('Date')  # sj = sj.rename(index={'Date'} или # sj = sj.reindex(sj.index.rename('Date'))
    #     # print("Данные sj после переиндексации time -> Date: ")
    #     # print(sj.head())
    #
    #     ''' Печать графика: '''
    #     # mpf.plot(data, type='candle')
    #     # mpf.plot(data, type='candle', mav=(3, 6, 9), volume=True, show_nontrading=True)
    #     mpf.plot(data, type=type, volume=volume, title=title)
    #
    # ''' Обработка ошибок '''
    # def badRequestError(self):
    #     # print('Обнаружена ошибка: ', error)   # class 'tinkoff.invest.exceptions.RequestError':
    #     # print(error.code, error.details, error.metadata)
    #     return error

if __name__ == '__main__':
    t_systems = TinSystems()
    print("Тест")
    ''' Создаем или обновляем данные об инструментах в json-файле '''
    # systems.create_figi_tickers_json_file()
    print(t_systems.readJson())

