import os
import sys
rootPath = os.getcwd() + '/../'
sys.path.append(rootPath)
import configparser
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

    connV1 = MySQLConn(config['mysql_azure'])
    connV2 = MySQLConn(config['mysql_azureV2'])

    logger = get_logger(logPath, f"{filename}.log")

    month = 10
    year = 2023
    with connV1.cursor() as cursorV1:
        schema = 'mgmtETL'
        cursorV1.execute(f"USE {schema}")
        sqlCommand = f"""
            SELECT SUBSTRING_INDEX(table_name, '_', 1) as tbl_name FROM information_schema.tables WHERE table_schema = '{schema}' group by tbl_name
        """
        cursorV1.execute(sqlCommand)
        for (res, ) in cursorV1.fetchall():

            cursorV1.execute(f"SHOW CREATE TABLE {res};")
            with connV2.cursor() as cursorV2:
                cursorV2.execute(f"USE {schema}")
                for (table, createTable) in cursorV1.fetchall():
                    
                    cursorV2.execute(createTable)

                    sqlCommand = f"""
                        SELECT * FROM {table};
                    """
                    cursorV1.execute(sqlCommand)
                    for row in cursorV1.fetchall():
                        replace_sql = f"""
                            REPLACE INTO {table} VALUES {str(row).replace('None', 'NULL')}
                        """
                        cursorV2.execute(replace_sql)





    connV1.close()
    connV2.close()