import telebot
from classes import *
from telebot import types
from sql import *
import ParsTeacher

#Ветка приватная, не ссыте оставлять ключ
#Ключ от ScheduleBot: 6062185576:AAGwpqVz0K8Zg_i7hz-URE2USZcxazuGN-A
#Ключ от тестового бота: 6026851226:AAFm4TvYE9QfIYSzx-hKiB3Mh_CtQ0KXrvY
bot = telebot.TeleBot("6026851226:AAFm4TvYE9QfIYSzx-hKiB3Mh_CtQ0KXrvY")
bot_id = bot.get_me().id
#region Клавиатуры
def GetPrepodsKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    ScheduleButton = types.KeyboardButton(text="Посмотреть мое расписание🗒️")
    BackButton = types.KeyboardButton(text="◀️")
    keyboard.add(ScheduleButton,BackButton)
    ExitButton = types.KeyboardButton(text="Я не преподаватель❌")
    keyboard.add(ExitButton)
    return keyboard
@staticmethod
def GetGroupsKeyboard():
    # Создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=False,one_time_keyboard=True)
    for i in Database.GetAllGroups():
        Button = types.KeyboardButton(text=i[0])
        keyboard.add(Button)
    return keyboard

@staticmethod
def GetSettingsKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    ScheduleButton = types.KeyboardButton(text="Изменить группу")
    BackButton = types.KeyboardButton(text="◀️")
    keyboard.add(ScheduleButton,BackButton)
    return keyboard
@staticmethod
def GetFreePrepodsKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=False)
    
    for i in Database.GetFreePrepods():
        Button = types.KeyboardButton(text=i[0])
        keyboard.add(Button)
    return keyboard
@staticmethod
def GetMenuKeyboard(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    ScheduleButton = types.KeyboardButton(text="Расписание 📝")
    SettingsButton = types.KeyboardButton(text="⚙️")
    keyboard.add(ScheduleButton,SettingsButton)
    if Database.is_user_activeprepod(message.chat.id)[0]:
        PrepodPanelButton = types.KeyboardButton(text="Панель преподавателя 🎓")
        keyboard.add(PrepodPanelButton)
    return keyboard
@staticmethod
def GetDatesKeyboard():
    # Создаем клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    # Создаем кнопки для нескольких дней
    for i in range(1,7):
        date = (datetime.datetime.now()+datetime.timedelta(days=i)).strftime('%d.%m.20%y')
        button_day = types.InlineKeyboardButton(text=date, callback_data=date)
        keyboard.add(button_day)
    return keyboard
@staticmethod
def GetPrepodDatesKeyboard(FIO):
    # Создаем клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    # Создаем кнопки для нескольких дней
    date = datetime.datetime.now().strftime('%d.%m.20%y')
    button_day = types.InlineKeyboardButton(text='Сегодня', callback_data=date+'*'+FIO)
    keyboard.add(button_day)
    for i in range(1,7):
        date = (datetime.datetime.now()+datetime.timedelta(days=i)).strftime('%d.%m.20%y')
        button_day = types.InlineKeyboardButton(text=date, callback_data=date+'*'+FIO)
        keyboard.add(button_day)
    return keyboard
#endregion
#region Панель преподавателей
@bot.message_handler(regexp='Панель преподавателя 🎓')
def DeletePrepod(message):
    PrepodPanel(message)
@bot.message_handler(regexp='Я не преподаватель❌')
def DeletePrepod(message):
    Database.RemovePrepodUser(message.chat.id)
    MainMenu(message)
@staticmethod
def PrepodPanel(message):
    response = Database.is_user_activeprepod(message.chat.id)
    print(response)
    if response[0]:
        FIO = Database.GetPrepodById(response[1])
        bot.send_message(message.chat.id,text='Здравствуйте '+FIO,reply_markup=GetPrepodsKeyboard())
    else:
        bot.send_message(message.chat.id,text='Вы не зарегестрированы как преподаватель, выберите свое ФИО',reply_markup=GetFreePrepodsKeyboard())
@bot.message_handler(regexp='Посмотреть мое расписание🗒️')
def GetPrepodsSchedule(message):
    FIO = Database.GetPrepodById(message.chat.id)
    bot.send_message(message.chat.id,text='Выберите дату на которое вам нужно получить расписание',reply_markup=GetPrepodDatesKeyboard(FIO))

@bot.message_handler(regexp='^[А-ЯЁ][а-яё]*(?:[\s-][А-ЯЁ][а-яё]*)*(?: [А-ЯЁ]\.(?:[А-ЯЁ]\.?)?)?$')
def RegPrepod(message):
    Database.RegPrepod(message.chat.id,message.text)
    PrepodPanel(message)

@bot.message_handler(commands=['pr'])
def PrepodPassword(message):
    password = message.text.split(' ')[1]
    if password == '123456':
        PrepodPanel(message)
    else:
        bot.send_message(message.chat.id, text='Неверный пароль')
        
#endregion
#region Навигация пользователя по менюшкам

@bot.message_handler(regexp='◀️')
def BackToMenuBtn_Handler(message):
    MainMenu(message)

@bot.message_handler(regexp='⚙️')
def SettingsBtn_Handler(message):
    SettingsMenu(message)

@bot.message_handler(regexp='Изменить группу')
def ChangeGroupBtn_Handler(message):
    bot.send_message(message.chat.id,text='Выберите свою новую группу',reply_markup=GetGroupsKeyboard())
#endregion
#region Менюшки
@staticmethod 
def MainMenu(message):
    bot.send_message(message.chat.id,text='Меню',reply_markup=GetMenuKeyboard(message))
def SettingsMenu(message):
    bot.send_message(message.chat.id,text='Настройки',reply_markup=GetSettingsKeyboard())
#endregion
#region Старт и регистрация
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id,text="Здравствуйте, я - бот для расписания KCPTScheduleBot")
    if not Database.is_user_exists(message.chat.id):
        bot.send_message(message.chat.id,text='Вы не зарегестрированы, выберите свою группу',reply_markup=GetGroupsKeyboard())
        return
    MainMenu(message)
@bot.message_handler(regexp='^.*\s([0-9]+(-[0-9]+)+)$')
def on_group_change(message):
    Database.RegUser(message.chat.id,message.text)
    MainMenu(message)
#endregion
#region Функционал расписаний
@bot.message_handler(regexp='Расписание 📝')
def ScheduleButton_handler(message):
    bot.send_message(message.chat.id,text='Выберите дату на которое вам нужно получить расписание',reply_markup=GetDatesKeyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    print(call.message.chat.id)
    if '*' in call.data:
        try:
            Pars_result = ParsTeacher.GetTeacherSchedule(DATE=call.data.split('*')[0],FIO=call.data.split('*')[1])
        except:
            bot.send_message(call.message.chat.id,text='Расписание на эту дату не найдено')
            return
        image = getScheduleAsImg(Pars_result)
        image.save('table.png')
        with open('table.png', 'rb') as f:
            bot.send_photo(call.message.chat.id,photo=f)
    else:
        try:
            Pars_result = GetDaySchedule(Data=call.data,Group=Database.GetGroupByUserId(call.message.chat.id))
        except IndexError:
            bot.send_message(call.message.chat.id,text='Расписание на эту дату не найдено')
            return
        image = getScheduleAsImg(Pars_result[0])
        if Pars_result[1]:
            bot.send_message(call.message.chat.id,text='Возможны ошибки, изменения в расписании не найдены или неполные, ответ стоит перепроверить вручную')
        image.save('table.png')
        with open('table.png', 'rb') as f:
            bot.send_photo(call.message.chat.id,photo=f)
#endregion
#region Старт бота
@staticmethod
def StartBot():
    bot.polling()
#endregion