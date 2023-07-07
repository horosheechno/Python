# база календаря
calendar_db: dict = {}

# класс корп.действий
class KD:
    def __init__(self, date: str = '',
                 isin: str = '',
                 ticker: str = '',
                 type_kd: str = '',
                 name: str = '',
                 end_date='Нет данных'):
        self.date = date
        self.isin = isin
        self.ticker = ticker
        self.type_kd = type_kd
        self.name = name
        self.end_date = end_date

    def __str__(self) -> str:
        return '==================\n' \
                'Тип: ' + self.type_kd + '\n' \
                'Название: ' + self.name + '\n' \
                'Тикер: ' + self.ticker.upper() + '\n' \
                'ISIN: ' + self.isin.upper() + '\n' \
                'Дата: ' + self.date + '\n' \
                'Дата окончания: ' + self.end_date +'\n' \
                '==================='
    def clear(self):
        self.date = ''
        self.isin = ''
        self.ticker = ''
        self.type_kd = ''
        self.name = ''
        self.end_date = 'Нет данных'


#a: KD = KD('dgdf', 'dgfdfb', 'fdgdfdf', 'fgdgd', 'dfggdf')

#print(a)