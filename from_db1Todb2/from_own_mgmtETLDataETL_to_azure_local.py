from connection.mysql_connection import MySQLConn
from utils.util import get_logger

import configparser

filename = __file__
last_slash = filename.rfind('/')
logFile = filename[last_slash+1:-2]+'log'

logger = get_logger('./log/', logFile)


config = configparser.ConfigParser()
config.read("config.ini")

conn_own = MySQLConn(config['mysql_own'])
with conn_own.cursor() as cursor:
    sqlCommand = "SELECT * FROM mgmtETL.DataETL WHERE siteID IN (7, 8)"
    cursor.execute(sqlCommand)
    result = cursor.fetchall()

conn_own.close()

conn_azure = MySQLConn(config["mysql_azure"])

with conn_azure.cursor() as cursor:
    for row in result:
        (
        siteId, name, description, deviceId, deviceType, deviceLogic, gatewayId, remark
        ) = row

        if remark is None:
            sqlCommand = f"""INSERT INTO mgmtETL.DataETL(siteId, name, description, deviceId, deviceType, deviceLogic, gatewayId) VALUES ('{siteId}', '{name}', '{description}', '{deviceId}', '{deviceType}', '{deviceLogic}', '{gatewayId}')"""
        else:
            sqlCommand = f"""INSERT INTO mgmtETL.DataETL(siteId, name, description, deviceId, deviceType, deviceLogic, gatewayId, remark) VALUES ('{siteId}', '{name}', '{description}', '{deviceId}', '{deviceType}', '{deviceLogic}', '{gatewayId}', {remark})"""
        logger.info(sqlCommand)
        cursor.execute(sqlCommand)
        logger.info(f"INSERT {row} Succeed")

conn_azure.close()