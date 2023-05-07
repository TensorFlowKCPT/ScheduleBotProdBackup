# Документация на TeleBot
https://github.com/eternnoir/pyTelegramBotAPI
# Еще ссылка, можно отсюда тянуть примеры
https://habr.com/ru/articles/442800/

# Работа с SQL
import sqlite3

# подключение к базе данных (если ее нет, то она будет создана автоматически)
conn = sqlite3.connect('users.db')

# создание таблицы
conn.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        variable1 TEXT,
        variable2 INTEGER
    )
''')

conn.commit()
conn.close()
# Затем вы можете использовать SQL-запросы для добавления, изменения или получения переменных пользователя:

import sqlite3

def set_variable1(user_id, variable1):
    conn = sqlite3.connect('users.db')
    conn.execute('INSERT OR REPLACE INTO users (user_id, variable1) VALUES (?, ?)', (user_id, variable1))
    conn.commit()
    conn.close()

def get_variable1(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.execute('SELECT variable1 FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None