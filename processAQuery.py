import os
import sys
rootPath = os.getcwd()
sys.path.append(rootPath)
import configparser
import pandas as pd
import time

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
        query = input("Please enter a query: ")
        while True:
            if ';' in query:
                break
            query += ' ' + input("If you finish typing query, please add ';'")
        print(query)
        try:
            startRunTime = time.time()
            cursor.execute(query)
            result = cursor.fetchall()
            print(len(result))
            df = pd.DataFrame(result)
            df.to_csv("processAQuery.csv")
            endRunTime = time.time()
            # for res in result:
            #     print(res)

        except Exception as ex:
            print(f'Please check your query, and the error message: {ex}')
            startRunTime = 0
            endRunTime = 0
    conn.close()
    
    print(f'time used: {endRunTime-startRunTime}')