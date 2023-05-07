import datetime
class Schedule():
    '''
    Создает объект расписания, с которым можно работать или дать боту на вывод, принимает
    Дату:datetime
    Список уроков:list
    Класс уроков содержит свойство 'Number' для того чтобы упростить этот класс, ведь расписание может содержать окна
    '''
    def __init__(self,Date:datetime,Uroki:list):
        self.Date = Date
        self.Uroki = Uroki