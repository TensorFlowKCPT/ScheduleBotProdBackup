import telebot
from classes import *
from telebot import types
from sql import *

#Ветка приватная, не ссыте оставлять ключ
#Ключ от ScheduleBot: 6062185576:AAGwpqVz0K8Zg_i7hz-URE2USZcxazuGN-A
#Ключ от тестового бота: 6026851226:AAFm4TvYE9QfIYSzx-hKiB3Mh_CtQ0KXrvY
bot = telebot.TeleBot("6026851226:AAFm4TvYE9QfIYSzx-hKiB3Mh_CtQ0KXrvY")
bot_id = bot.get_me().id

@staticmethod
def GetGroupsKeyboard():
    # Создаем клавиатуру
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=False)
    for i in Database.GetAllGroups():
        Button = types.KeyboardButton(text=i[0])
        keyboard.add(Button)
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

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id,text="Здравствуйте, я - бот для расписания KCPTScheduleBot")
    if not Database.is_user_exists(message.chat.id):
        bot.send_message(message.chat.id,text='Вы не зарегестрированы, выберите свою группу',reply_markup=GetGroupsKeyboard())
        return
    bot.send_message(message.chat.id,text='Выберите дату на которое вам нужно получить расписание',reply_markup=GetDatesKeyboard())
    

@bot.message_handler(regexp='^.*\s([0-9]+(-[0-9]+)+)$')
def message_handler(message):
    Database.RegUser(message.chat.id,message.text)
    bot.send_message(message.chat.id,text='Выберите дату на которое вам нужно получить расписание',reply_markup=GetDatesKeyboard())
    


# Обработчик нажатия на кнопку
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    #Тут якобы получаем из базы/парсера 
    '''
     Schedule = parsKCPT.GetSchedule(call.data,)
    ''' 
    print(call.message.chat.id)
    Pars_result = GetDaySchedule(Data=call.data,Group=Database.GetGroupByUserId(call.message.chat.id))
    image = getScheduleAsImg(Pars_result[0])
    if Pars_result[1]:
        bot.send_message(call.message.chat.id,text='Возможны ошибки, изменения в расписании не найдены или неполные, ответ стоит перепроверить вручную')
    image.save('table.png')
    with open('table.png', 'rb') as f:
        bot.send_photo(call.message.chat.id,photo=f)
    

@staticmethod
def StartBot():
    bot.polling()
