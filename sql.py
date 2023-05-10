import sqlite3

class Database:
    @staticmethod
    def CreateGroup(Group: str):
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute("INSERT INTO Groups (GroupName) VALUES (?)", (Group,))
    @staticmethod
    def CreatePrepod(Prepod: str):
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute("INSERT INTO Prepods (PrepodFIO) VALUES (?)", (Prepod,))

    @staticmethod
    def RegUser(ChatId, Group: str):
        with sqlite3.connect('ScheduleBot.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM Groups WHERE GroupName = ?", (Group,))
            result = c.fetchone()
            if result:
                group_id = result[0]
            else:
                return

            # Добавляем нового пользователя в таблицу Users
            c.execute('''
    INSERT INTO Users (id, group_id)
    VALUES (?, ?)
    ON CONFLICT (id) DO UPDATE SET group_id = EXCLUDED.group_id;
''', (ChatId, group_id))
            conn.commit()
    @staticmethod
    def RegPrepod(ChatId, PrepodFIO: str):
        with sqlite3.connect('ScheduleBot.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM Prepods WHERE PrepodFIO = ?", (PrepodFIO,))
            result = c.fetchone()
            if result:
                prepod_id = result[0]
            else:
                return

            # Добавляем нового пользователя в таблицу Prepods
            c.execute('''
    INSERT INTO PrepodUsers (id, prepod_id)
    VALUES (?, ?)
    ON CONFLICT (id) DO UPDATE SET prepod_id = EXCLUDED.prepod_id;
''', (ChatId, prepod_id))
            conn.commit()
    @staticmethod
    def GetAllGroups():
        with sqlite3.connect('ScheduleBot.db') as conn:
            c = conn.cursor()
            c.execute("SELECT GroupName FROM Groups")
            return c.fetchall()
        
    @staticmethod
    def GetFreePrepods():
        with sqlite3.connect('ScheduleBot.db') as conn:
            c = conn.cursor()
            c.execute('''SELECT p.PrepodFIO
    FROM Prepods p
    LEFT JOIN PrepodUsers u ON p.id = u.prepod_id
    WHERE u.id IS NULL
            ''')
            return c.fetchall()

    
    @staticmethod
    def Execute(query: str, params: dict = None):
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute(query, params) if params else conn.execute(query)
            result = cursor.fetchone()
            if result:
                return cursor.fetchall()
            else:
                return result
    @staticmethod
    def RemovePrepodUser(id):
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute("DELETE FROM PrepodUsers WHERE id=?", (id,))
        
    @staticmethod
    def GetGroupByUserId(ChatId):
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute("SELECT Groups.GroupName FROM Users INNER JOIN Groups ON Users.group_id = Groups.id WHERE Users.id=?", (ChatId,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
    @staticmethod
    def GetPrepodById(user_id):
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute('''SELECT Prepods.PrepodFIO
FROM PrepodUsers
JOIN Prepods ON PrepodUsers.prepod_id = Prepods.id
WHERE PrepodUsers.id = ?;''', (user_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        


    @staticmethod
    def is_user_activeprepod(user_id):
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute("""
    SELECT u.id, COALESCE(p.PrepodFIO, NULL) AS PrepodFIO
    FROM PrepodUsers u
    LEFT JOIN Prepods p ON u.prepod_id = ?
""", (user_id,))
            result = cursor.fetchone()
            if result:
                return [True,result[0]]
            else:
                return [False,None]
    @staticmethod
    def is_user_exists(user_id):
        with sqlite3.connect('ScheduleBot.db') as conn:
          c = conn.cursor()
          c.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
          result = c.fetchone()
          return result is not None
    @staticmethod
    def StartDatabase():
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute('''
                 DROP TABLE IF EXISTS Groups
                ''')
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute('''
                 DROP TABLE IF EXISTS Prepods
                ''')
        # with sqlite3.connect('ScheduleBot.db') as conn:
        #     conn.execute('''
        #          DROP TABLE IF EXISTS Users
        #         ''')
        
        #Создание таблицы с группами
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute('''
                 CREATE TABLE IF NOT EXISTS Groups (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   GroupName TEXT NOT NULL
                   )
                ''')
        Groups = ['АТ 20-11', 
                  'АТ 21-11', 
                  'АТ 22-11', 
                  'ДО 20-11-1', 
                  'ДО 20-11-2', 
                  'ДО 21-11-1', 
                  'ДО 21-11-2', 
                  'ДО 22-11-1', 
                  'ДО 22-11-2', 
                  'ИБАС 21-11', 
                  'ИБАС 22-11', 
                  'ИСиП 20-11-1', 
                  'ИСиП 20-11-2', 
                  'ИСиП 20-11-3', 
                  'ИСиП 21-11-1', 
                  'ИСиП 21-11-2', 
                  'ИСиП 21-11-3', 
                  'ИСиП 22-11-1', 
                  'ИСиП 22-11-2', 
                  'ИСиП 22-11-3', 
                  'КП 20-11-1', 
                  'КП 20-11-2', 
                  'КП 20-11-3', 
                  'КП 20-11-4', 
                  'КП 21-11-1', 
                  'КП 21-11-2', 
                  'КП 21-11-3', 
                  'КП 22-11-1', 
                  'КП 22-11-2', 
                  'КП 22-11-3', 
                  'КП 22-11-4', 
                  'ОСАТПиП 20-11-1', 
                  'ОСАТПиП 20-11-2', 
                  'ОСАТПиП 21-11', 
                  'ОСАТПиП 22-11', 
                  'ПДО ТТ 20-11', 
                  'ПДО ТТ 21-11', 
                  'ПДО ТТ 22-11', 
                  'ССА 20-11-1', 
                  'ССА 20-11-2', 
                  'ССА 20-11-3', 
                  'ССА 21-11-1', 
                  'ССА 21-11-2', 
                  'ССА 21-11-3', 
                  'ССА 22-11-1', 
                  'ССА 22-11-2']
        for i in Groups:
            Database.CreateGroup(i)
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute('''
                 CREATE TABLE IF NOT EXISTS Prepods (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   PrepodFIO TEXT NOT NULL
                   )
                ''')
        Prepods = [
        'Айметдинов Б.И.', 
        'Андреева С.Р.', 
        'Арефьев Е.А.', 
        'Ахметов Р.А.', 
        'Базыгунова Е.Р.', 
        'Байкина И.Л.', 
        'Бекмагамбетова Д..', 
        'Бекшенева Г.Х.', 
        'Белевич В.Ю.', 
        'Богданова П.А.', 
        'Бородина С.В.', 
        'Бочанов В.Ф.', 
        'Бочанцева Л.И.', 
        'Васильева Е.Н.', 
        'Вешкурцева А.А.', 
        'Вибе М.И.', 
        'Воронцова Т.В.', 
        'Вохменцева Т.Н.', 
        'Галимзянов С.С.', 
        'Гейер А.Р.', 
        'Гуляев И.П.', 
        'Гурьянова Н.А.', 
        'Давыдова А.Е.', 
        'Елисеева Я.А.', 
        'Замятина С.М.', 
        'Звонарева И.М.', 
        'Ибуков Д.В.', 
        'Ивлева А.Е.', 
        'Казакова О.Н.', 
        'Калаев А.П.', 
        'Калугина С.В.', 
        'Камитова А.И.', 
        'Каранкевич В.В.', 
        'Каранкевич В..', 
        'Климович Н.П.', 
        'Коротков Н.И.', 
        'Корчагина-Мокеева А.Г.', 
        'Косыгина Т.Н.', 
        'Куденова В.Д.', 
        'Кузнецов А.С.', 
        'Кузьмин М.С.', 
        'Кучина И.А.', 
        'Кучумина Д.Т.', 
        'Лизовенко Я.И.', 
        'Литус Л.С.', 
        'Малов В.Н.', 
        'Машкина В.А.', 
        'Мельникова Е.С.', 
        'Михеева Л.В.', 
        'Мосол С.В.', 
        'Муканова О.М.', 
        'Мясников Д.А.', 
        'Насрутдинова Л.С.', 
        'Норматов Ш.Ш.', 
        'Павлова А.В.', 
        'Павлова Н.Г.', 
        'Панамарева И.А.', 
        'Пермякова Л.П.', 
        'Плашинова Е.А.', 
        'Погорельская И.Ю',
        'Погорельская О.Ю.',
        'Полищук А.А.',
        'Посредникова Е.А.',
        'Просверенникова С.А.',
        'Проскурякова А.А.',
        'Рагозина Т.М.',
        'Размазина Т.Е.',
        'Рассохина Н.Н.',
        'Рашевская С.Ф.',
        'Романенко С.В.',
        'Самарцева Р.Я.',
        'Сафонов М.М.',
        'Сергеев С.В.',
        'Ситникова К.И.',
        'Сушкова А.А.',
        'Тарасенко Т.П.',
        'Тимофеев П.Н.',
        'Ужанова Т.Л.',
        'Чемакина А.В.',
        'Черемисова Т.В.',
        'Черкасова Т.А.',
        'Чудная Л.Г.',
        'Швецов Е.В.',
        'Шестопалова Е.А.',
        'Шипунова О.В.',
        'Ярунова З.В.',
        'Админ А.А.'
        ]
        for i in Prepods:
            Database.CreatePrepod(i)
        #Создание таблицы пользователей с привилегиями преподавателей
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute('''
                 CREATE TABLE IF NOT EXISTS PrepodUsers (
                   id INTEGER PRIMARY KEY,
                   prepod_id INTEGER NOT NULL,
                   FOREIGN KEY (prepod_id) REFERENCES Prepods(id)
                   )
                ''')
        #Создание таблицы с пользователями
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute('''
                 CREATE TABLE IF NOT EXISTS Users (
                   id INTEGER PRIMARY KEY,
                   group_id INTEGER NOT NULL,
                   FOREIGN KEY (group_id) REFERENCES Groups(id)
                   )
                ''')
#Database.StartDatabase()
#with sqlite3.connect('ScheduleBot.db') as conn:
#            c = conn.cursor()
#            c.execute("SELECT * FROM Users")
#            print(c.fetchall())
            