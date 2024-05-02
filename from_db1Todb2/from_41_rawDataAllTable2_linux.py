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

    conn_41 = MySQLConn(config['mysql_41'])
    conn_linux = MySQLConn(config['mysql_linux_server'])

    logger = get_logger(logPath, f"{filename}.log")

    month = 10
    year = 2023
    with conn_41.cursor() as cursor41:
        schema = "rawData"
        sqlCommand = f"""
            SELECT SUBSTRING_INDEX(table_name, '_', 1) as tbl_name FROM information_schema.tables WHERE table_schema = '{schema}{year}' group by tbl_name
        """
        cursor41.execute(sqlCommand)
        for (table, ) in cursor41.fetchall():
            logger.debug(table)
            start = 0

            while True:
                
                value_string = ''
                end = start+30000
                sqlCommand = f"""
                    SELECT * FROM {schema}{year}.{table}_{month} WHERE GWts >= '2023-10-15' AND GWts < '2023-10-16' LIMIT {start}, {end};
                """
                start += 30000
                cursor41.execute(sqlCommand)
                if cursor41.rowcount == 0:
                    logger.info("No more to INSERT")
                    break
                with conn_linux.cursor() as cursor_linux:
                    column_names = [desc[0] for desc in cursor41.description]
                    # column_names = "(" + ", ".join(column_names) + ")
                    for row in cursor41.fetchall():
                        value_string += "("
                        for i, r in enumerate(row):
                            if type(r) == datetime.datetime:
                                if column_names[i] == 'GWts':
                                    ts = r.strftime("%Y-%m-%d %H:%M:%S.%f")
                                else:
                                    ts = r.strftime("%Y-%m-%d %H:%M:%S")
                                value_string += "'" + ts + "', "
                            elif r is None:
                                value_string += "NULL, "
                            else:
                                value_string += f"'{r}', "
                            if i+1 == len(column_names):
                                value_string = value_string[:-2]
                        value_string += "), "
                        
                        if len(value_string) > 10**6:
                            logger.info(f"Value string is greater than 1,000,000, {len(value_string):,}")
                            value_string = value_string[:-2]
                            replace_sql = f"""
                                REPLACE INTO {schema}.{table} VALUES {value_string}
                            """
                            cursor_linux.execute(replace_sql)
                            logger.info("REPLACE Succeed!")
                            value_string = ''
                    
                    if value_string != '':
                        logger.info("Processing REPLACE")
                        value_string = value_string[:-2]
                        
                        replace_sql = f"""
                            REPLACE INTO {schema}.{table} VALUES {value_string}
                        """
                        cursor_linux.execute(replace_sql)
                        logger.info("REPLACE Succeed!")


    conn_41.close()
    conn_linux.close()