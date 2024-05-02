import os
import sys
rootPath = os.getcwd()
sys.path.append(rootPath)
import configparser

from connection.mysql_connection import MySQLConn
from utils.util import get_logger

if __name__ == '__main__':
    file = __file__
    basename = os.path.basename(file)
    filename = os.path.splitext(basename)[0]
    logPath = os.getcwd()+ '/log'

    config = configparser.ConfigParser()
    config.read(rootPath+'/config.ini')

    conn1 = MySQLConn(config['mysql_azure'])
    conn2 = MySQLConn(config['mysql_azureV2'])

    logger = get_logger(logPath, f"{filename}.log")

    with conn1.cursor() as cursor:
        schema = "rawData2023"
        cursor.execute(f"SHOW TABLES FROM {schema}")

        for (res, ) in cursor.fetchall():
            cursor.execute(f"SHOW CREATE TABLE {schema}.{res}")
            (table, createTable) = cursor.fetchone()
            with conn2.cursor() as cursor2:
                cursor2.execute(f"USE {schema};")
                cursor2.execute(createTable)

    with conn1.cursor() as cursor:
        logger.info("------- Processing rawData -------")
        schema = "rawData"
        cursor.execute(f"SHOW TABLES FROM {schema};")

        for (res, ) in cursor.fetchall():
            
            cursor.execute(f'SHOW CREATE TABLE {schema}.{res}')
            (table, createTable) = cursor.fetchone()
            
            # if table.lower() == table and table != 'calculation':
            with conn2.cursor() as cursor2:
                cursor2.execute(f"USE {schema};")
                cursor2.execute(createTable)


    conn1.close()
    conn2.close()

    # conn_wsl = MySQLConn(config['mysql_own'])

    # logger = get_logger(logPath, f"{filename}.log")
    
    # with conn_wsl.cursor() as cursor:
    #     cursor.execute("SHOW TABLES FROM rawData")

    #     for (res, ) in cursor.fetchall():
    #         cursor.execute(f"SHOW CREATE TABLE rawData.{res}")

    #         (table, createTable) = cursor.fetchone()
    #         cursor.execute("USE rawData2023;")
    #         for i in range(1, 13):
    #             month = '{:02}'.format(i)
    #             write_table = table+'_'+month
    #             new_createTable = createTable.replace(table, write_table)
    #             cursor.execute(new_createTable)
    # conn_wsl.close()