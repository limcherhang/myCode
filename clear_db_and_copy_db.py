## 這只程式會drop掉目標db的所有schema和table，不要隨便用
from connection.mysql_connection import MySQLConn
from utils.util import get_logger
import os

import configparser
import datetime

def drop_all_schema(cursor, config, ignore_db):
    cursor.execute("SHOW DATABASES;")
    while True:
        print(f'請你確認是否要將以下配置的database的所有schema drop掉?')
        print(f"host: {config['host']}")
        print(f"port: {config['port']}")
        print(f"user: {config['user']}")
        print(f"password: {config['password']}")
        print("是的話請輸入yes/Y(大小寫不拘)")
    
        reply = input()
        reply = reply.lower()
        if reply == "yes" or reply == 'y':
            break
        else:
            raise "請檢查好後再執行"

    for (db, ) in cursor.fetchall():
        if db in ignore_db:
            continue
        cursor.execute(f"DROP DATABASE {db}")
        


file = __file__
basename = os.path.basename(file)
logFile = os.path.splitext(basename)[0]+'.log'

logger = get_logger('./log/', logFile)

config = configparser.ConfigParser()
config.read("config.ini")

ignore_db = ('sys', 'information_schema', 'performance_schema', 'mysql', 'logETL')

conn_azure = MySQLConn(config["mysql_azure"])
conn_own = MySQLConn(config['mysql_own'])
with conn_azure.cursor() as cursor_azure:
    with conn_own.cursor() as cursor_own:
        #################################################### 小心使用 不要drop錯 不然很麻煩
        drop_all_schema(cursor_own, config['mysql_own'], ignore_db)
        ####################################################

        cursor_azure.execute('SHOW DATABASES;')
        for res in cursor_azure.fetchall():
            db = res[0]
            if db in ignore_db:
                continue
            
            logger.debug(f"DB: {db}")
            cursor_own.execute("SHOW DATABASES;")
            if (db, ) not in cursor_own.fetchall():
                cursor_own.execute(f"CREATE DATABASE {db}")

            cursor_azure.execute(f'USE {db};')
            cursor_azure.execute(f"SHOW TABLES;")
            
            cursor_own.execute(f"USE {db}")

            for table in cursor_azure.fetchall():
                table = table[0]
                cursor_azure.execute(f'SHOW CREATE TABLE {table}')
                for _, create_info in cursor_azure.fetchall():
                    cursor_own.execute(create_info)

                cursor_azure.execute(f"SELECT * FROM {table}")
                
                columns = [col[0] for col in cursor_azure.description]
 
                for row in cursor_azure.fetchall():
                    row = list(row)
                    for index, item in enumerate(row):
                        if type(item) == datetime.datetime:
                            if item.microsecond != 0:
                                row[index] = row[index].strftime("%Y-%m-%d %H:%M:%S.%f")
                            else:
                                row[index] = row[index].strftime("%Y-%m-%d %H:%M:%S")
                    row = ['NULL' if value is None else (f"'{value}'" if isinstance(value, (str, datetime.datetime)) else str(value)) for value in row]

                    sql = f"INSERT INTO {table}({', '.join(['`' + col + '`' for col in columns])}) VALUES ({', '.join(row)})"
                    logger.debug(sql)

                    cursor_own.execute(sql)
    
conn_azure.close()
conn_own.close()