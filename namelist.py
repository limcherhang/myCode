import os
import sys
rootPath = os.getcwd()
sys.path.append(rootPath)
import configparser
import pandas as pd

from utils.util import get_logger
from connection.mysql_connection import MySQLConn

if __name__ == '__main__':

    file = __file__
    basename = os.path.basename(file)
    filename = os.path.splitext(basename)[0]
    logPath = os.getcwd()+ '/log'

    config = configparser.ConfigParser()
    config.read(rootPath+'/config.ini')

    conn = MySQLConn(config['mysql_fn'])

    logger = get_logger(logPath, f"{filename}.log")

    filename = 'NameList.xlsx'
    xls = pd.ExcelFile(filename)
    sheet_names = xls.sheet_names

    for name in sheet_names:
        df = pd.read_excel(filename, sheet_name=name)
        df = df.fillna(value='NoValue')
        df = df.to_dict(orient='index') 

        for i, row in df.items():
            cols = [col.replace('-', '_') for col in row.keys()]
            cols = '`, `'.join(cols)
            cols = '`' + cols + '`'
            values = [val.replace('-', '_') if val != 'NoValue' else 'NULL' for val in row.values()]
            values = "', '".join(values)
            values = "'" + values + "'"
            values = values.replace("'NULL'", 'NULL')

            query = f"""
                INSERT INTO dataPlatform.NameList{name} (siteId, {cols}) VALUES (86, {values})
            """
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query)
            except Exception as ex:
                print(ex)
                print(query)
                print(row)
                print('------------------------------------------------------------------------------------')