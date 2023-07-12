class InfoSlave():
    def __init__(self):
        pass

    ''' Проверка на отсутствие времени (исходное программное время)'''
    def check_notime(self, daytime=str()):
        # print('datetime: ', daytime)
        if daytime == '01.01.1970 03:00':
            return '--'
        else: return daytime


    ''' Основные биржи, для выделения их в списке'''
    def exchanges_main(self):
        # description = Description()
        # return [description.exchanges('MOEX'), description.exchanges('SPB'),]
        return ['MOEX', 'SPB']