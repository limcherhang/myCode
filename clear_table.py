from connection.mysql_connection import MySQLConn
from utils.util import get_logger
import os

import configparser
import time

file = __file__
basename = os.path.basename(file)
logFile = os.path.splitext(basename)[0]+'.log'

logger = get_logger('./log/', logFile)

config = configparser.ConfigParser()
config.read("config.ini")

i = 0
bacnet = 0
zigbee = 0
modbus = 0

while True:
    if i % 10 == 0:
        try:
            conn_azure.close()
            time.sleep(60)
        except:
            pass
        conn_azure = MySQLConn(config["mysql_azure"])
        try:
            with conn_azure.cursor() as cursor:
                cursor.execute('SHOW PROCESSLIST;')
                for res in cursor.fetchall():
                    if 'Sleep' in res and res[5] > 600:
                        logger.debug(res)
                        cursor.execute(f"KILL {res[0]};")
        except Exception as ex:
            logger.error(f"iter {i} sql failed: {ex}")
    if i % 50 == 0:
        try:
            with conn_azure.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM rawData.bacnet;")
                (count, ) = cursor.fetchone()
            if count == 0:
                bacnet = 1
            with conn_azure.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM rawData.modbus;")
                (count, ) = cursor.fetchone()
            if count == 0:
                modbus = 1
            with conn_azure.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM rawData.zigbee;")
                (count, ) = cursor.fetchone()
            if count == 0:
                zigbee = 1
        except Exception as ex:
            logger.error(f"iter {i} sql failed: {ex}")
    
    s = time.time()
    try:
        with conn_azure.cursor() as cursor:
            # cursor.execute("DELETE FROM logETL.logEntries WHERE fileName LIKE 'MQTT%' or  filename='PPSS.log'  LIMIT 1000")
            if bacnet == 0:
                cursor.execute("DELETE FROM rawData.bacnet LIMIT 1000")
            if modbus == 0:
                cursor.execute("DELETE FROM rawData.modbus LIMIT 1000")
            if zigbee == 0:
                cursor.execute("DELETE FROM rawData.zigbee LIMIT 1000")
    except Exception as ex:
        logger.error(f"iter {i} sql failed: {ex}")
    e = time.time()
    time.sleep(3)
    logger.debug(f'iter {i} time used: {e-s}')
    i+=1

    if bacnet == 1 and modbus == 1 and zigbee == 1:
        break

    

conn_azure.close()