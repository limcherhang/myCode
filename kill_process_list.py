from connection.mysql_connection import MySQLConn
from utils.util import get_logger
import os

import configparser
import datetime

file = __file__
basename = os.path.basename(file)
logFile = os.path.splitext(basename)[0]+'.log'

logger = get_logger('./log/', logFile)

config = configparser.ConfigParser()
config.read("config.ini")

conn_azure = MySQLConn(config["mysql_fn_azure"])

with conn_azure.cursor() as cursor:

    cursor.execute('SHOW PROCESSLIST;')
    for res in cursor.fetchall():
        if 'Sleep' in res and res[5] > 600 and res[3] == 'sys':
            logger.debug(res)
            cursor.execute(f"KILL {res[0]};")

conn_azure.close()
