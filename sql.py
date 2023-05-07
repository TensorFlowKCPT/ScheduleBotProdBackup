import sqlite3

class Database:
    @staticmethod
    def CreateGroup(Group: str):
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute("INSERT INTO Groups (GroupName) VALUES (?)", (Group,))

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
    def GetAllGroups():
        with sqlite3.connect('ScheduleBot.db') as conn:
            c = conn.cursor()
            c.execute("SELECT GroupName FROM Groups")
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
    def GetGroupByUserId(ChatId):
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute("SELECT Groups.GroupName FROM Users INNER JOIN Groups ON Users.group_id = Groups.id WHERE Users.id=?", (ChatId,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
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
            