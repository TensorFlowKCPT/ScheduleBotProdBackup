import datetime
from PIL import Image, ImageDraw, ImageFont
from functools import lru_cache
import textwrap
from ScheduleClass import Schedule
from UrokClass import Urok
from ParsForExcel import GetExcelSchedule,parstable
from ParsForWord import GetWordSchedule
import numpy

# Работает, лайк за то что все мега просто, как варик можно прикрутить кастомизацию
@staticmethod
def getScheduleAsImg(Schedule):
    header = ["Урок", "Предмет", "Кабинет", "Преподаватель", "Время"]
    table_data = []
    for urok in Schedule.Uroki:
        max_width = 20
        name_lines = textwrap.wrap(urok.Name, max_width)
        kabinet_lines = textwrap.wrap(str(urok.Kabinet), max_width)
        prepod_lines = textwrap.wrap(str(urok.Prepod), max_width)
        row = [urok.Number, name_lines, kabinet_lines, prepod_lines, GetUrokTime(Schedule.Date,urok.Number)]
        table_data.append(row)

    y = 30 * sum([max([len(row[i]) for i in range(1, 4)]) for row in table_data]) + len(table_data) + 1
    image = Image.new('RGB', (1350, y + 350), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('arial.ttf', size=18)

    x = 10
    y = 10

    cell_width = 265
    cell_height = 30

    for i in range(len(header)):
        draw.rectangle((x, y, x + cell_width, y + 30), outline=(0, 0, 0))
        draw.text((x + 5, y + 5), header[i], font=font, fill=(0, 0, 0))
        x += cell_width

    x = 10
    y += cell_height

    for row in table_data:
        max_lines = max([len(row[i]) for i in range(1, 4)])
        for i in range(len(row)):
            draw.rectangle((x, y, x + cell_width, y + cell_height * (max_lines+1)), outline=(0, 0, 0))
            if i == 0:
                draw.text((x + 5, y + 5), str(row[i]), font=font, fill=(0, 0, 0))
            elif i == 1 or i == 2 or i == 3:
                for j, line in enumerate(row[i]):
                    draw.text((x + 5, y + 5 + j * cell_height), line, font=font, fill=(0, 0, 0))
            else:
                draw.text((x + 5, y + 5), str(row[i]), font=font, fill=(0, 0, 0))
            x += cell_width
        x = 10
        y += cell_height * (max_lines+1)

    return image



#Метод который вернет правильное расписание на определенный день, совместив расписание из ексель и из ворда
cache = {}
@staticmethod
def GetDaySchedule(Group:str, Data:str):
    date_format = '%d.%m.%Y'
    Date = datetime.datetime.strptime(Data, date_format)

    cache_key = f'{Group}-{Data}'
    if cache_key in cache:
        cached_schedule, cached_time = cache[cache_key]
        time_since_last_update = datetime.datetime.now() - cached_time
        if time_since_last_update < datetime.timedelta(hours=12):
            return [cached_schedule,False]

    FinalSchedule = Schedule(Date, [])
    excel_schedule = GetExcelSchedule(parstable(Data, Group), Group).Uroki
    word_result = GetWordSchedule(Data,Group)
    word_schedule = word_result[0].Uroki
    final_uroki = []

    # Пройти по урокам из Excel расписания и добавить их в список final_uroki
    for urok_data in excel_schedule:
        urok = Urok(Number=urok_data.Number, Name=urok_data.Name, Kabinet=urok_data.Kabinet, Prepod=urok_data.Prepod)
        final_uroki.append(urok)

    # Пройти по урокам из Word расписания и добавить их в список final_uroki
    for urok_data in word_schedule:
        urok = Urok(Number=urok_data.Number, Name=urok_data.Name, Kabinet=urok_data.Kabinet, Prepod=urok_data.Prepod)
        urok_date = word_result[0].Date
        urok_exists = False
        for i, final_urok in enumerate(final_uroki):
            if final_urok.Number == urok.Number:
                final_uroki[i] = urok
                urok_exists = True
        if not urok_exists:
            final_uroki.append(urok)

    # Добавить список final_uroki в объект FinalSchedule
    FinalSchedule.Uroki = final_uroki
    cache[cache_key] = (FinalSchedule, datetime.datetime.now())
    return [FinalSchedule,word_result[1]]
    
    
        

    
#Работает, очень простой метод который перенаправляет в другой
@staticmethod
def TranslateDateTimeDay(Date:datetime):
    '''
    Переводит дату из dateTime в str с днем недели в формате "Пятница"
    '''
    return TranslateStrDay(Date.strftime('%A'))
#Работает, лучше не менять, максимально просто и локанично
@staticmethod
def TranslateStrDay(Day:str):
    '''
    Переводит день на английском в формате str("Friday") в str с днем недели в формате str("Пятница")
    '''
    Days = {'Monday':"Понедельник",
            'Tuesday':'Вторник',
            'Wednesday':'Среда',
            'Thursday':'Четверг',
            'Friday':'Пятница',
            'Saturday':'Суббота',
            'Sunday':"Воскресенье"
            }
    return Days[Day]


#Проверено, работает, не трогать, из вариков можно сделать метод который будет сразу принимать день недели в формате str("Friday"), но не вижу смысла
@staticmethod
def GetUrokTime(Date:datetime,UrokNumber:int):
    '''
    Принимает дату и порядковый номер урока (Именно в этом порядке, иначе вернет None)
    Возвращает время урока в формате str("8:15-9:00")
    '''
    NormalList = {1:"8:15-9:00",
                  2:"9:00-9:45",
                  3:"9:55-10:40",
                  4:"10:40-11:25",
                  5:"11:40-12:25",
                  6:"12:25-13:10",
                  7:"13:30-14:15",
                  8:"14:15-15:00",
                  9:"15:15-16:00",
                  10:"16:00-16:45",
                  11:"16:55-17:40",
                  12:"17:40-18:25"}
    SubbotaList = {1:"8:15-9:00",
                   2:"9:00-9:45",
                   3:"9:50-10:35",
                   4:"10:35-11:20",
                   5:"11:35-12:20",
                   6:"12:20-13:05",
                   7:"13:20-14:05",
                   8:"14:05-14:50",
                   9:"15:05-15:50",
                   10:"15:50-16:35",
                   11:"16:40-17:25",
                   12:"17:25-18:10"}
    if Date.strftime('%A')=='Saturday':
        return SubbotaList[int(UrokNumber)]
    else:
        return NormalList[int(UrokNumber)]



#for i in GetDaySchedule("ИСиП 21-11-3", "01.05.2023").Uroki:
#    print(i.Number,i.Name,i.Prepod,i.Kabinet)