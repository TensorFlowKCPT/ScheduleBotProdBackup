import telebot
from classes import *
from telebot import types
from sql import *

#Ветка приватная, не ссыте оставлять ключ
#Ключ от ScheduleBot: 6062185576:AAGwpqVz0K8Zg_i7hz-URE2USZcxazuGN-A
#Ключ от тестового бота: 6026851226:AAFm4TvYE9QfIYSzx-hKiB3Mh_CtQ0KXrvY
bot = telebot.TeleBot("6026851226:AAFm4TvYE9QfIYSzx-hKiB3Mh_CtQ0KXrvY")
bot_id = bot.get_me().id
#region Клавиатуры
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
    SettingsButton = types.KeyboardButton(text="🔙")
    keyboard.add(ScheduleButton,SettingsButton)
    return keyboard

@staticmethod
def GetMenuKeyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    ScheduleButton = types.KeyboardButton(text="Расписание 📝")
    SettingsButton = types.KeyboardButton(text="⚙️")
    keyboard.add(ScheduleButton,SettingsButton)
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
#endregion
#region Навигация пользователя по менюшкам
@bot.message_handler(regexp='🔙')
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
    bot.send_message(message.chat.id,text='Меню',reply_markup=GetMenuKeyboard())
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