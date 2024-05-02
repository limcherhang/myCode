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

    from_conn = MySQLConn(config['mysql_fn_azure'])
    conn = MySQLConn(config['mysql_fn_azure'])

    # schema = 'dataPlatform'
    # year = '2024'

    # with conn.cursor() as cursor:
    #     # cursor.execute(f"USE {schema};")
    #     sqlCommand = f"SHOW TABLES FROM {schema}"
    #     cursor.execute(sqlCommand)

    #     for (table, ) in cursor.fetchall():
    #         cursor.execute(f"SHOW CREATE TABLE {schema}.{table}")
    #         (_, createTable) = cursor.fetchone()

    #         for i in range(1, 13):
                
    #             month = f"{i:02}"
    #             ct = createTable.replace('`'+table+'`', schema + year + '.`'+ table + '_' + month + '`', 1)
    #             try:
    #                 cursor.execute(ct)
    #             except Exception as ex:
    #                 print(ct)
    #                 print(ex)
    #                 print()
                
    # schema = 'reportplatform'

    # with from_conn.cursor() as from_cursor:
    #     sqlCommand = f"SHOW TABLES FROM {schema};"
    #     from_cursor.execute(sqlCommand)
    #     with conn.cursor() as cursor:
    #         cursor.execute(f"USE {schema}")
    #         for (table, ) in from_cursor.fetchall():
    #             from_cursor.execute(f"SHOW CREATE TABLE {schema}.{table};")
    #             (_, createTable) = from_cursor.fetchone()
    #             cursor.execute(createTable)

    # conn.close()
    # from_conn.close()

    schema = ['dataPlatform', 'reportPlatform']
    year_now = '2024'
    year_after = ['2025', '2026', '2027', '2028', '2029', '2030']

    with conn.cursor() as cursor:
        for sc in schema:
            for i in range(len(year_after)):
                try:
                    cursor.execute(f"DROP DATABASE {sc+year_after[i]}")
                except:
                    pass
                try:
                    cursor.execute(f"CREATE DATABASE {sc+year_after[i]}")
                except:
                    pass

                sqlCommand = f"SHOW TABLES FROM {sc+year_now}"
                cursor.execute(sqlCommand)

                for (table, ) in cursor.fetchall():
                    print(year_after[i], sc, table)
                    cursor.execute(f"SHOW CREATE TABLE {sc+year_now}.{table}")
                    (_, createTable) = cursor.fetchone()
                    cursor.execute(f"USE {sc+year_after[i]}")
                    cursor.execute(createTable)
