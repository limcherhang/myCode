import os
import sys
rootPath = os.getcwd() + '/../'
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

    conn_azure = MySQLConn(config['mysql_fn_azure'])
    conn_linux = MySQLConn(config['mysql_linux_server'])

    logger = get_logger(logPath, f"{filename}.log")

    with conn_azure.cursor() as cursor:
        months = ("09", "10")
        sqlCommand = f"""
            SELECT SUBSTRING_INDEX(table_name, '_', 1) as tbl_name FROM information_schema.tables WHERE table_schema = 'dataPlatform2023' group by tbl_name
        """
        cursor.execute(sqlCommand)
        modules = cursor.fetchall()

        for (module, ) in modules:
            
            logger.info(f"----------- Processing {module} ---------")
            for month in months:
                value_string = ''
                sqlCommand = f"""
                    SELECT * FROM dataPlatform2023.{module}_{month}
                """
                cursor.execute(sqlCommand)
                result = cursor.fetchall()

                for res in result:
                    res = list(res)
                    res[0] = res[0].strftime("%Y-%m-%d %H:%M:%S")
                    res = tuple(res)
                    value_string += str(res).replace("None", "NULL") + ', '
                    
                    if len(value_string) > 10**6:
                        logger.info(f"Value string is greater than 1,000,000, {len(value_string):,}")
                        value_string = value_string[:-2]
                        with conn_linux.cursor() as cursor_linux:
                            replace_sql = f"""
                                REPLACE INTO dataPlatform.{module} VALUES
                                {value_string}
                            """
                            # logger.debug(replace_sql)
                            cursor_linux.execute(replace_sql)
                            logger.info("REPLACE Succeed!")

                        value_string = ''


                if value_string != '':
                    logger.info("Processing REPLACE")
                    value_string = value_string[:-2]

                    with conn_linux.cursor() as cursor_linux:
                        replace_sql = f"""
                            REPLACE INTO dataPlatform.{module} VALUES
                            {value_string}
                        """
                        cursor_linux.execute(replace_sql)
                        logger.info("REPLACE Succeed!")
                        
            logger.info(f"----------- Processing {module} Succeed ---------")




    conn_azure.close()
    conn_linux.close()