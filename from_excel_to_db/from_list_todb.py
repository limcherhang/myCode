import os
import sys
rootPath = os.getcwd() + '/../'
sys.path.append(rootPath)
import configparser
import datetime
import pandas as pd

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

    read_file = 'powerList.xlsx'

    DataETL = pd.read_excel(read_file, sheet_name='DataETL')
    print(DataETL)

    DeviceLogic = pd.read_excel(read_file, sheet_name='DeviceLogic')
    print(DeviceLogic)

    DataETL = [row for row in DataETL.itertuples(index=False, name=None)]

    value_string = ''
    for row in DataETL:
        value_string += str(row).replace('nan', 'NULL') + ', '
    
    if value_string != '':
        value_string = value_string[:-2]

        with conn.cursor() as cursor:
            replace_sql = f"""
                REPLACE INTO mgmtETL.DataETL VALUES {value_string}
            """
            cursor.execute(replace_sql)

    DeviceLogic = [row for row in DeviceLogic.itertuples(index=False, name=None)]

    value_string = ''
    for row in DeviceLogic:
        value_string += str(row).replace('nan', 'NULL') + ', '
    
    # if value_string != '':
    #     value_string = value_string[:-2]

    #     with conn.cursor() as cursor:
    #         replace_sql = f"""
    #             REPLACE INTO mgmtETL.DeviceLogic VALUES {value_string}
    #         """

    #         cursor.execute(replace_sql)
    