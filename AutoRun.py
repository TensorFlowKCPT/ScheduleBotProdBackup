import ScheduleBot
import sql
import logging
import parsKCPT
import threading
import time

def Downloader():
    while True:
      print('Загрузка данных с сайта')
      logging.info('Загрузка данных с сайта')
      parsKCPT.Download()
      time.sleep(3*60*60)
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Старт бота')
sql.Database.StartDatabase()
downloader = threading.Thread(target = Downloader)
downloader.start()
logging.info('Бот запущен')
print('Бот запущен')
while True:
  try:
        ScheduleBot.StartBot()
  except Exception as e:
       print(e)
       logging.info("***ERROR***: Произошло исключение: %s", str(e))
downloader.join()
        