import requests
import configparser
import datetime
import time
import schedule

from connection.mysql_connection import MySQLConn
from utils.util import get_logger

def post(token, message):
    headers = { "Authorization": "Bearer " + token }
    data = { 'message': message }

    requests.post("https://notify-api.line.me/api/notify", headers = headers, data = data)

def do_post_message(token, result):
    for (ts, fileName, path, level, message) in result:
        if '7: Broker' in message:
            continue
        else:
            print(message)
            msg = "\n"
            msg += f"ts: {ts} \n"
            msg += f"fileName: {fileName}\n"
            msg += f"path: {path} \n"
            msg += f"level: {level}\n"
            msg += f"message: {message}"

            post(token, msg)

def runTask():

    logger = get_logger('./log/', 'log_tracker.log')    

    token = 'NIdAv1llqhqFTD83JERtgFYXq605SByoabDKPvDqbku'

    config = configparser.ConfigParser()
    config.read("config.ini") 

    conn = MySQLConn(config['mysql_azure'])

    now = datetime.datetime.now().replace(second=0, microsecond=0)

    start_time = now - datetime.timedelta(minutes=5)

    with conn.cursor() as cursor:
        logger.debug("track ERROR")
        sql1 = f"SELECT * FROM logETL.logEntries WHERE level='ERROR' AND fileName LIKE 'MQTT%' AND ts >= '{start_time}' AND ts <'{now}';"
        cursor.execute(sql1)
        result = cursor.fetchall()
        if result:
            do_post_message(token, result)
        logger.debug(sql1)

    if now.minute == 5:
        start_time = start_time.replace(minute=0)
        with conn.cursor() as cursor:
            logger.debug('track PPSS dataETL')
            sql9 = f"SELECT * FROM logETL.logEntries WHERE level='ERROR' AND fileName='PPSS.log' AND ts >= '{start_time}' AND ts <'{now}';"
            cursor.execute(sql9)
            result = cursor.fetchall()
            if result:
                do_post_message(token, result)
            logger.debug(sql9)


# 创建一个排程对象
s = schedule.Scheduler()

# 定义要运行任务的分钟列表
target_minutes = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

# 添加定时任务（在指定的分钟运行，秒数设为0）
for minute in target_minutes:
    s.every().hour.at(f":{minute:02}").do(runTask)

# 开始运行排程
while True:
    s.run_pending()
    time.sleep(1)