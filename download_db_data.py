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

    with conn.cursor() as cursor:
        i = 28900000
        while True:
            query = f"""
                SELECT * FROM rawData2023.zigbee_11 LIMIT {i}, 50000;
            """

            cursor.execute(query)
            if cursor.rowcount == 0:
                break
            result = ()
            for res in cursor.fetchall():
                value_string = ()
                for r in res:
                    if type(r) == datetime.datetime:
                        value_string += (r.strftime("%Y-%m-%d %H:%M:%S.%f"),)
                    elif r == None:
                        value_string += ("NULL", )
                    else:
                        value_string += (r, )
                result += (value_string, )

            df = pd.DataFrame(result)
            df.to_csv(f"result_{i}.csv")
            logger.debug(i)
            i+= 50000

    
    conn.close()