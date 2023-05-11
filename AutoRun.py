import ScheduleBot
import sql
import logging
import parsKCPT


print('Загрузка данных с сайта')
#parsKCPT.Download()
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Старт бота')
sql.Database.StartDatabase()
logging.info('Бот запущен')
print('Бот запущен')

while True:
  try:
        ScheduleBot.StartBot()
  except Exception as e:
       print(e)
       logging.info("***ERROR***: Произошло исключение: %s", str(e))

        