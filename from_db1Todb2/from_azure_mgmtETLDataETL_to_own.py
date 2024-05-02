from connection.mysql_connection import MySQLConn
from utils.util import get_logger

import configparser

filename = __file__
last_slash = filename.rfind('/')
logFile = filename[last_slash+1:-2]+'log'

logger = get_logger('./log/', logFile)


config = configparser.ConfigParser()
config.read("config.ini")


conn_azure = MySQLConn(config["mysql_azure"])

with conn_azure.cursor() as cursor_42:
    sqlCommand = "SELECT * FROM mgmtETL.DataETL;"
    cursor_42.execute(sqlCommand)
    result = cursor_42.fetchall()

conn_azure.close()

conn_own = MySQLConn(config["mysql_own"])

with conn_own.cursor() as cursor_own:
    cursor_own.execute("SET SQL_SAFE_UPDATES = 0;")
    cursor_own.execute("DELETE FROM mgmtETL.DataETL;")
    cursor_own.execute("SET SQL_SAFE_UPDATES = 1;")
    for row in result:
        (
        siteId, name, description, deviceId, deviceType, deviceLogic, gatewayId, remark
        ) = row
        if remark is None:
            sqlCommand = f"""INSERT INTO mgmtETL.DataETL(siteId, name, description, deviceId, deviceType, deviceLogic, gatewayId) VALUES ('{siteId}', '{name}', '{description}', '{deviceId}', '{deviceType}', '{deviceLogic}', '{gatewayId}')"""
        else:
            sqlCommand = f"""INSERT INTO mgmtETL.DataETL(siteId, name, description, deviceId, deviceType, deviceLogic, gatewayId, remark) VALUES ('{siteId}', '{name}', '{description}', '{deviceId}', '{deviceType}', '{deviceLogic}', '{gatewayId}', {remark})"""
        logger.info(sqlCommand)
        cursor_own.execute(sqlCommand)

        logger.info(f"INSERT {row} Succeed")


conn_own.close()