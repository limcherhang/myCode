import os
import sys
rootPath = os.getcwd()
sys.path.append(rootPath)
import configparser
import pandas as pd
import datetime

from connection.mysql_connection import MySQLConn
from utils.util import get_logger

if __name__ == '__main__':
    
    file = __file__
    basename = os.path.basename(file)
    filename = os.path.splitext(basename)[0]
    logPath = os.getcwd()+ '/log'

    config = configparser.ConfigParser()
    config.read(rootPath+'/config.ini')

    conn = MySQLConn(config['mysql_azureV2'])

    logger = get_logger(logPath, f"{filename}.log")

    schema = 'rawData2023'
    with conn.cursor() as cursor:
        sqlCommand = f"SHOW TABLES FROM {schema};"
        cursor.execute(sqlCommand)
        
        for (table, ) in cursor.fetchall():
            logger.debug(table)
            while True:
                delete_sql = f"DELETE FROM {schema}.{table} LIMIT 50000;"

                cursor.execute(delete_sql)
                
                _count = cursor.rowcount
                logger.debug(_count)
                if _count == 0:
                    break
    
    conn.close()