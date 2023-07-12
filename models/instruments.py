''' Модель Instruments '''
# from models.instruments_slave import InstrumentsSlave
from assets.arguments import Description
from goby_test import Goby
from models.systems import T_Systems

import asyncio
import datetime

class T_Instruments():
    def __init__(self):
        # self.instruments_slave = InstrumentsSlave()
        self.description = Description()
        self.goby = Goby()
        self.t_systems = T_Systems()

    async def get_instruments_info(self, tickers: list = None, figies: list = None):
        response_list = list()
        description = Description()

        if tickers is not None:
            ''' Получаем figi из файла данных json по его ticker '''
            if figies is None: figies = list()
            figi_: str = ''   # Определяем переменную для проверки ответа с данными после запроса
            for ticker in tickers:
                figi_ = self.t_systems.figi(ticker=ticker)
                if figi_: figies.append(figi_)
                figi_ = ''

        if figies is not None:
            for figi in figies:
                instrument_data = await self.goby.get_instrument_info(figi=figi)
                if instrument_data is None: break   # Проверка на пустое значение (не найден инструмент по figi)
                # response = client.instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id='BBG000B9XRY4')
                # response = await self.goby.get_instrument_info(figi=figi)
                # instrument_data = response.instrument
                # instrument_data = response.instrument
                # print('instrument_data: ', instrument_data)
                # Цены на начало дня и на текущее время:
                # print('datetime.datetime.today(): ', datetime.date.today())
                # Кол-во дней на графике
                days_for_chart = int(7)
                from_ = datetime.datetime.now() - datetime.timedelta(days=days_for_chart*3)
                # from_ = datetime.datetime(2022, 2, 20)
                # print('from_: ', from_)
                instrument_candles = await self.goby.get_stock_candles(figi=instrument_data.figi,
                                                            from_=from_,
                                                            to=datetime.datetime.now(),
                                                            interval=5)  # CANDLE_INTERVAL_DAY - '5' - 1 день.
                # print('instrument_candles: ', len(instrument_candles), instrument_candles)
                # Если недостаточно данных - увеличиваем число дней для запроса
                if len(instrument_candles) < days_for_chart:
                    from_ = datetime.datetime.now() - datetime.timedelta(days=days_for_chart * 10)
                    instrument_candles = await self.goby.get_stock_candles(figi=instrument_data.figi,
                                                                from_=from_,
                                                                to=datetime.datetime.now(),
                                                                interval=5)  # CANDLE_INTERVAL_DAY - '5' - 1 день.

                list_data = self.goby.createListData(instrument_candles)
                # print("list_data[0]['open']: ", list_data[0]['open'])
                # print("list_data[-1]['close']", list_data[-1]['close'])
                open_price = list_data[-1]['open']
                close_price = list_data[-1]['close']
                last_7days_prices = list()
                # Собираем последние цены:
                for i in range(days_for_chart, 0, -1):
                    # print('i=', i, f'list_data[{-i}]["close"]: ', list_data[-i]['close'])
                    last_7days_prices.append(list_data[-i]['close'])

                # print('last_7days_prices: ', last_7days_prices)
                # last_7days_prices = [list_data[days_for_chart*(-1)]['close'], list_data[days_for_chart*(-1)+1]['close'], list_data[days_for_chart*(-1)+2]['close'],
                #                     list_data[days_for_chart*(-1)+3]['close'], list_data[days_for_chart*(-1)+4]['close'], list_data[days_for_chart*(-1)+5]['close'], list_data[days_for_chart*(-1)+6]['close']
                #                     ]
                green = "rgba(50,205,50,1)"     # Цвет графика
                red = "rgba(220,20,60,1)"
                instrument_info = dict(figi=instrument_data.figi, ticker=instrument_data.ticker,
                                       class_code=instrument_data.class_code,
                                       name=instrument_data.name,
                                       sector=instrument_data.sector.capitalize(),
                                       # last_price=self.get_last_price(instrument_data.figi),
                                       open_price=open_price,
                                       close_price=close_price,
                                       last_7days_prices=last_7days_prices,
                                       green_or_red=green if last_7days_prices[-1] > last_7days_prices[0] else red,     # Цвет графика
                                       currency=description.currency_type(instrument_data.currency, flag='simbol'),
                                       exchange=instrument_data.exchange,
                                       trading_status=description.trading_status(instrument_data.trading_status),
                                       buy_available_flag=instrument_data.buy_available_flag,
                                       sell_available_flag=instrument_data.sell_available_flag,
                                       api_trade_available_flag=instrument_data.api_trade_available_flag,
                                       difference=round(close_price-open_price, 2),
                                       percent=round((close_price-open_price)/open_price*100, 2)
                                       )
                response_list.append(instrument_info)
        # print("response_list: ", response_list)
        else:
            print("Instruments: Заполните данные по запросу акции")
        return response_list
